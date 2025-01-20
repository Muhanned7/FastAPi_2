from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("x, y, result",[
    (3,5,8),
    (5,4,9),
    (3,6,9),
    (20,4,24)
])
def test_add(x,y,result):
    assert add(x,y) == result

def test_subtract():
    assert subtract(3,4) == -1

def test_multiply():
    assert multiply(2,3) == 6

def test_divide():
    assert divide(10,2) == 5


def test_bank_set_initial_amount(bank_account):
    
    assert bank_account.balance == 50

def test_bank_set_default_amount(zero_bank_account):
    
    assert zero_bank_account.balance == 0

def test_withdrawal(bank_account):
    
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6)==55


@pytest.mark.parametrize("deposit, withdraw, balance",[
    (200,100,100),
    (50,40,10),
    (300,60,240),
    (200,10,190)
])
def test_bank_transaction(zero_bank_account,deposit,withdraw,balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance==balance


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)