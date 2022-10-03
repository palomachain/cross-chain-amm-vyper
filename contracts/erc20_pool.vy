#@version 0.3.6

FACTORY: immutable(address)
TOKEN: immutable(address)
POOL_ID: immutable(uint256)

interface Factory:
    def swap_in(pool_id: uint256, amount: uint256, recipient: String[64]): nonpayable
    def add_liquidity(pool_id: uint256, amount: uint256, depositor: address): nonpayable

@internal
def _safe_transfer(_token: address, _to: address, _value: uint256):
    response: Bytes[32] = raw_call(
        _token,
        _abi_encode(
            _to,
            _value,
            method_id=method_id("transfer(address,uint256)")
        ),
        max_outsize=32
    ) # dev: failed transfer
    if len(response) > 0:
        assert convert(response, bool) # dev: failed transfer

@internal
def _safe_transfer_from(_token: address, _from: address, _to: address, _value: uint256):
    response: Bytes[32] = raw_call(
        _token,
        _abi_encode(
            _from,
            _to,
            _value,
            method_id=method_id("transferFrom(address,address,uint256)")
        ),
        max_outsize=32
    ) # dev: failed transferFrom
    if len(response) > 0:
        assert convert(response, bool) # dev: failed transferFrom

@external
def __init__(token: address, pool_id: uint256):
    FACTORY = msg.sender
    TOKEN = token
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
def add_liquidity(amount: uint256):
    self._safe_transfer_from(TOKEN, msg.sender, self, amount)
    Factory(FACTORY).add_liquidity(POOL_ID, amount, msg.sender)

@external
def swap_in(amount: uint256, chain_id: uint256, recipient: String[64]):
    self._safe_transfer_from(TOKEN, msg.sender, self, amount)
    Factory(FACTORY).swap_in(POOL_ID, amount, recipient)

@external
def swap_out(amount: uint256, recipient: address):
    assert msg.sender == FACTORY
    self._safe_transfer(TOKEN, recipient, amount)

@external
def remove_liquidity(amount: uint256, recipient: address):
    assert msg.sender == FACTORY
    self._safe_transfer(TOKEN, recipient, amount)
