import finnhub
import requests
import pickle
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from .models import Stock
from .forms import StockForm, RegistrationForm
from django.contrib.auth.models import User



# Finnhub API token
FINNHUB_API_KEY = 'ct0m6epr01qkfpo5q3tgct0m6epr01qkfpo5q3u0'
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# --- Export Portfolio (Safe) ---
@login_required
def export_portfolio(request):
    user_stocks = Stock.objects.filter(user=request.user)
    portfolio_data = [{
        'ticker': s.ticker,
        'shares': s.shares,
        'companyName': s.companyName,
        'latestPrice': s.latestPrice,
    } for s in user_stocks]

    serialized = pickle.dumps(portfolio_data)
    response = HttpResponse(serialized, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=portfolio.pkl'
    return response


def import_portfolio(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        try:
            data = pickle.load(uploaded_file)

            if not isinstance(data, list):
                messages.error(request, "Invalid file format.")
                return redirect("portfolio")

            for item in data:
                if not isinstance(item, dict):
                    continue  # Skip invalid entries

                Stock.objects.create(
                    user=request.user,
                    ticker=item.get("ticker"),
                    shares=item.get("shares"),
                    purchase_date=item.get("purchase_date"),
                )

            messages.success(request, "Portfolio imported successfully.")
        except Exception as e:
            messages.error(request, f"Deserialization error: {str(e)}")

    return redirect("portfolio")

# Utility function to handle N/A and empty values
def get_valid_value(value):
    if value in [None, 'N/A', '', 'null']:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0

# Finnhub API call
def search_stock(stock_ticker):
    try:
        # Fetch quote data
        quote_url = f'https://finnhub.io/api/v1/quote?symbol={stock_ticker}&token={FINNHUB_API_KEY}'
        quote_response = requests.get(quote_url)
        if quote_response.status_code != 200:
            return []
        quote_data = quote_response.json()

        # Fetch profile data
        profile_url = f'https://finnhub.io/api/v1/stock/profile2?symbol={stock_ticker}&token={FINNHUB_API_KEY}'
        profile_response = requests.get(profile_url)
        if profile_response.status_code != 200:
            return []
        profile_data = profile_response.json()

        # Log data for debugging
        print("Quote Data:", quote_data)
        print("Profile Data:", profile_data)

        # Extract data safely
        stock_data = [{
            'symbol': stock_ticker,
            'companyName': profile_data.get('name', 'N/A'),
            'marketCap': profile_data.get('marketCapitalization', None),
            'peRatio': profile_data.get('peBasicExclExtraTTM', None),  
            'week52High': quote_data.get('h', None),  
            'week52Low': quote_data.get('l', None),   
            'primaryExchange': profile_data.get('exchange', 'N/A'),
            'open': quote_data.get('o', None),
            'close': quote_data.get('c', None),
            'high': quote_data.get('h', None),
            'low': quote_data.get('l', None),
            'latestPrice': quote_data.get('c', None),
        }]
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return []


# Cache stock data fetching
def fetch_stock_info(stock_ticker):
    cache_key = f'stock_info_{stock_ticker}'
    stock_info = cache.get(cache_key)
    if stock_info is None:
        stock_info = search_stock(stock_ticker)
        cache.set(cache_key, stock_info, 3600)
    return stock_info

# Register new user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Home view
@login_required
def home(request):
    total_portfolio_value = 0
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        stocks = search_stock(stock_ticker)
        return render(request, 'home.html', {'stocks': stocks, 'total_portfolio_value': total_portfolio_value})
    stockdata = Stock.objects.filter(user=request.user)
    for stock in stockdata:
        stock_info = fetch_stock_info(stock.ticker)
        if stock_info:
            stock.latestPrice = stock_info[0].get('latestPrice', 0.0)
            stock.current_value = float(stock.latestPrice) * stock.shares
            stock.save()
            total_portfolio_value += stock.current_value
    return render(request, 'home.html', {'stockdata': stockdata, 'total_portfolio_value': total_portfolio_value})

# About page
@login_required
def about(request):
    return render(request, 'about.html')

# Portfolio page

@login_required
def portfolio(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_ticker = form.cleaned_data['ticker'].upper()
            stock_info = search_stock(stock_ticker)
            if stock_info:
                stock = form.save(commit=False)
                # Assign fetched stock data
                stock.symbol = stock_info[0].get('symbol', stock_ticker)
                stock.companyName = stock_info[0].get('companyName', 'Unknown Company')
                stock.marketCap = stock_info[0].get('marketCap', 0.0)
                stock.peRatio = stock_info[0].get('peRatio', 0.0)
                stock.week52High = stock_info[0].get('week52High', 0.0)
                stock.week52Low = stock_info[0].get('week52Low', 0.0)
                stock.returnYTD = stock_info[0].get('returnYTD', 0.0)
                stock.previousClose = stock_info[0].get('previousClose', 0.0)
                stock.latestPrice = stock_info[0].get('latestPrice', 0.0)
                
                # Calculate the stock's current value
                stock.current_value = stock.latestPrice * stock.shares
                stock.user = request.user
                stock.save()

                messages.success(request, f"{stock.symbol} ({stock.companyName}) added successfully.")
            else:
                messages.warning(request, f"Ticker {stock_ticker} does not exist.")
        else:
            messages.warning(request, 'Please correct the form errors.')

    # After saving the stock, fetch the portfolio data
    stockdata = Stock.objects.filter(user=request.user)
    total_portfolio_value = 0
    for stock in stockdata:
        stock_info = fetch_stock_info(stock.ticker)
        if stock_info:
            stock.latestPrice = stock_info[0].get('latestPrice', 0.0)
            stock.current_value = stock.latestPrice * stock.shares
            stock.save()  # Save the updated stock
            total_portfolio_value += stock.current_value

    return render(request, 'portfolio.html', {'stockdata': stockdata, 'total_portfolio_value': total_portfolio_value})




@login_required
def delete_stock(request, id):
    try:
        stock = Stock.objects.get(id=id)
        if request.method == 'POST':
            stock.delete()
            return redirect('portfolio')
    except Stock.DoesNotExist:
        print(f"Stock with id {id} does not exist.")
        return redirect('portfolio')


@login_required
def store_data_in_session(request):
    # Store user-specific data in sessions
    request.session['user_id'] = request.user.id
    request.session['username'] = request.user.username

    return HttpResponse("Data stored in session.")

@login_required
def retrieve_data_from_session(request):
    # Retrieve user-specific data from sessions
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    if user_id and username:
        return HttpResponse(f"User ID: {user_id}, Username: {username}")
    else:
        return HttpResponse("User-specific data not found in session.")

@login_required
def stock_results(request):
    stocks = None
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        stocks = search_stock(stock_ticker)

    return render(request, 'stock_results.html', {'stocks': stocks})



@login_required
def get_portfolio_value(request):
    total_portfolio_value = 0
    stockdata = Stock.objects.filter(user=request.user)
    for stock in stockdata:
        stock_info = fetch_stock_info(stock.ticker)  # Fetch updated stock info
        if stock_info:
            stock.latestPrice = stock_info[0].get('latestPrice', 0.0)
            stock.current_value = stock.latestPrice * stock.shares
            stock.save()
            total_portfolio_value += stock.current_value
    return JsonResponse({'total_portfolio_value': total_portfolio_value})
