#@version 0.3.6

FACTORY: immutable(address)
POOL_ID: immutable(uint256)
TOKEN: constant(address) = empty(address)

interface Factory:
    def swap_in(pool_id: uint256, amount: uint256, recipient: String[64]): nonpayable
    def add_liquidity(pool_id: uint256, amount: uint256, depositor: address): nonpayable

@external
def __init__(pool_id: uint256):
    FACTORY = msg.sender
    POOL_ID = pool_id

@external
@pure
def factory() -> address:
    return FACTORY

@external
@pure
def token() -> address:
    return TOKEN

@external
@pure
def pool_id() -> uint256:
    return POOL_ID

@external
@payable
@nonreentrant("L")
def add_liquidity(amount: uint256):
    if msg.value == amount:
        Factory(FACTORY).add_liquidity(POOL_ID, amount, msg.sender)
    elif msg.value > amount:
        send(msg.sender, msg.value - amount)
        Factory(FACTORY).add_liquidity(POOL_ID, amount, msg.sender)
    else:
        raise "Insufficient funds"

@external
@payable
@nonreentrant("L")
def swap_in(amount: uint256, recipient: String[64]):
    if msg.value == amount:
        Factory(FACTORY).swap_in(POOL_ID, amount, recipient)
    elif msg.value > amount:
        send(msg.sender, msg.value - amount)
        Factory(FACTORY).swap_in(POOL_ID, amount, recipient)
    else:
        raise "Insufficient funds"

@external
@nonreentrant("L")
def swap_out(amount: uint256, recipient: address):
    assert msg.sender == FACTORY
    send(recipient, amount)

@external
@nonreentrant("L")
def remove_liquidity(amount: uint256, recipient: address):
    assert msg.sender == FACTORY
    send(recipient, amount)
