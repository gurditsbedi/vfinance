from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum

from .forms import registration, loginForm, quoteForm, buyAndSellForm
from .models import user, transactionTable
from .utils import lookup

def indexPage(request):
    if request.user.is_authenticated and request.user.id is not None:
        cash = user.objects.get(user_id=int(request.user.id)).cash
        stocksOfUser = transactionTable.objects.filter(user_id=int(request.user.id))\
                                               .values('symbol', 'name')\
                                               .annotate(shares=Sum('shares'))\
                                               .order_by('symbol')
        allTotal = float(cash)
        for stock in stocksOfUser:
            stock['price'] = lookup(stock['symbol'])['price']
            stock['total'] = round(stock['price'] * stock['shares'], 2)
            allTotal += stock['total']
            stock['total'] = '{:.2f}'.format(round(stock['total'], 2))
        allTotal = '{:.2f}'.format(round(allTotal, 2))

        return render(request, 'finance/index.html', {'userLoggedIn': True,
                                                      'stocksOfUser': stocksOfUser,
                                                      'allTotal': allTotal,
                                                      'cash': cash})
    else:
        userLoggedIn = False
        return HttpResponseRedirect(reverse('loginPage'), {'userLoggedIn': userLoggedIn})


def registerPage(request):
    userLoggedIn = request.user.is_authenticated and request.user.id is not None
    if request.method == 'POST':
        form = registration(request.POST)
        if form.is_valid():
            userDjango = User(username=form.cleaned_data['username'],
                              password=make_password(form.cleaned_data['password']))
            userDjango.save()
            user_extended = user(cash=25000, user_id=userDjango.id)
            user_extended.save()
            userAuth = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
            userLoggedIn = request.user.is_authenticated and request.user.id is not None
            if userAuth is not None:
                login(request, userAuth)
                userLoggedIn = True
            return HttpResponseRedirect(reverse('indexPage'), {'userLoggedIn': userLoggedIn})
    else:
        form = registration()
        userLoggedIn = request.user.is_authenticated and request.user.id is not None
    return render(request, 'finance/register.html', {'form': form, 'userLoggedIn': userLoggedIn})


def loginPage(request):
    userLoggedIn = False
    if request.method == 'POST':
        logout(request)
        form = loginForm(request.POST)
        if form.is_valid():
            userDjango = User(username=form.cleaned_data['username'],
                              password=form.cleaned_data['password'])
            userAuth = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
            if userAuth is not None:
                login(request, userAuth)
                userLoggedIn = True
            return HttpResponseRedirect(reverse('indexPage'), {'userLoggedIn': userLoggedIn})
    else:
        form = loginForm()
    return render(request, 'finance/login.html', {'form': form, 'userLoggedIn': userLoggedIn})


def logoutPage(request):
    logout(request)
    messages.info(request, 'Logged Out Successfully.')
    return HttpResponseRedirect(reverse('loginPage'), {'userLoggedIn': False})


@login_required(login_url=reverse_lazy('loginPage'))
def quotePage(request):
    if request.method == 'POST':
        form = quoteForm(request.POST)
        someError = True
        info = None
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            info = lookup(symbol)
            # if we get the stock price properly
            if info['price']: someError = False

        return render(request, 'finance/quoted.html', {'userLoggedIn': True,
                                                       'info': info,
                                                       'error': someError})
    else:
        form = quoteForm()
        return render(request, 'finance/quote.html', {'userLoggedIn': True,
                                                      'form': form})


@login_required(login_url=reverse_lazy('loginPage'))
def buyPage(request):
    if request.method == 'POST':
        form = buyAndSellForm(request.POST)
        if form.is_valid():
            # data collection
            info = form.cleaned_data['stockInfo']

            cashRequired = float(form.cleaned_data['shares']) * float(info['price'])
            userInusertable = user.objects.get(user_id=int(request.user.id))
            canBuy = True if userInusertable.cash >= cashRequired else False
            if canBuy:
                p = transactionTable.objects.create(symbol=form.cleaned_data['symbol'],
                                                    name=info['name'],
                                                    shares=form.cleaned_data['shares'],
                                                    price=info['price'],
                                                    user_id=request.user.id)
                userInusertable.cash = float(userInusertable.cash) - cashRequired
                p.save()
                userInusertable.save()
                messages.info(request, 'Bought!')
                return HttpResponseRedirect(reverse('indexPage'))
            else:
                messages.info(request, 'Can\'t afford.')
                return render(request, 'finance/buy.html', {'userLoggedIn': True,
                                                            'form': form})
    else:
        form = buyAndSellForm()
    return render(request, 'finance/buy.html', {'userLoggedIn': True, 'form': form})


@login_required(login_url=reverse_lazy('loginPage'))
def sellPage(request):
    if request.method == 'POST':
        form = buyAndSellForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data['stockInfo']
            ans = transactionTable.objects.filter(symbol=info['symbol'])\
                                          .values('name', 'symbol')\
                                          .annotate(shares=Sum('shares'))
            if not ans:
                messages.info(request, 'No shares of that symbol in your portfolio.')
                return render(request, 'finance/sell.html', {'userLoggedIn': True, 'form': form})

            userInusertable = user.objects.get(user_id=int(request.user.id))
            cashEarned = float(form.cleaned_data['shares']) * float(info['price'])
            canSell = True if form.cleaned_data['shares'] <= ans[0]['shares'] else False
            if canSell:
                 p = transactionTable.objects.create(symbol=form.cleaned_data['symbol'],
                                                    name=info['name'],
                                                    shares= 0-int(form.cleaned_data['shares']),
                                                    price=info['price'],
                                                    user_id=request.user.id)
                 userInusertable.cash = float(userInusertable.cash) + cashEarned
                 p.save()
                 userInusertable.save()
                 messages.info(request, 'Sold!')
                 return HttpResponseRedirect(reverse('indexPage'))
            else:
                messages.info(request, 'You don\'t have that much amount of shares of that symbol.')
                return render(request, 'finance/sell.html', {'userLoggedIn': True,
                                                            'form': form})
    else:
        form = buyAndSellForm()
    return render(request, 'finance/sell.html', {'userLoggedIn': True, 'form': form})

@login_required(login_url=reverse_lazy('loginPage'))
def historyPage(request):
    if request.user.is_authenticated and request.user.id is not None:
        stocksOfUser = transactionTable.objects.filter(user_id=int(request.user.id))\
                                               .order_by('trnDateTime')
        return render(request, 'finance/history.html', {'userLoggedIn': True,
                                                        'stocksOfUser': stocksOfUser})

