# @version 0.3.7

ETH_POOL_BLUEPRINT: immutable(address)
ERC20_POOL_BLUEPRINT: immutable(address)
GOVERNANCE: immutable(address)

event AddLiquidity:
    pool_id: indexed(uint256)
    token: address
    amount: uint256
    depositor: indexed(address)
    recipient: String[64]

event SwapIn:
    pool_id: uint256
    token: address
    amount: uint256
    recipient: String[64]

event SwapOut:
    pool_id: indexed(uint256)
    amount: uint256
    recipient: address

event RemoveLiquidity:
    pool_id: indexed(uint256)
    amount: uint256
    recipient: address

event FeeWithdrawn:
    pool_id: indexed(uint256)
    amount: uint256
    recipient: address

pool_addresses: public(HashMap[uint256, HashMap[address, address]])
admin: public(address)

interface Pool:
    def swap_out(amount: uint256, recipient: address): nonpayable
    def remove_liquidity(amount: uint256, recipient: address): nonpayable

@external
def __init__(compass_evm: address, eth_pool_blueprint: address, erc20_pool_blueprint: address, governance: address):
    self.admin = compass_evm
    ETH_POOL_BLUEPRINT = eth_pool_blueprint
    ERC20_POOL_BLUEPRINT = erc20_pool_blueprint
    GOVERNANCE = governance

@external
def create_pool(token: address, pool_id: uint256):
    assert self.pool_addresses[pool_id][token] == empty(address), "Existing pool"
    pool: address = empty(address)
    if token == empty(address):
        pool = create_from_blueprint(ETH_POOL_BLUEPRINT, pool_id)
    else:
        pool = create_from_blueprint(ERC20_POOL_BLUEPRINT, token, pool_id)
    self.pool_addresses[pool_id][token] = pool

@external
def add_liquidity(pool_id: uint256, token: address, amount: uint256, depositor: address, recipient: String[64]):
    assert self.pool_addresses[pool_id][token] == msg.sender, "Wrong pool ID"
    log AddLiquidity(pool_id, token, amount, depositor, recipient)

@external
def swap_in(pool_id: uint256, token: address, amount: uint256, recipient: String[64]):
    assert self.pool_addresses[pool_id][token] == msg.sender, "Wrong pool ID"
    log SwapIn(pool_id, token, amount, recipient)

@external
def swap_out(pool_id: uint256, token: address, amount: uint256, recipient: address):
    assert msg.sender == self.admin
    Pool(self.pool_addresses[pool_id][token]).swap_out(amount, recipient)
    log SwapOut(pool_id, amount, recipient)

@external
def remove_liquidity(pool_id: uint256, token: address, amount: uint256, recipient: address):
    assert msg.sender == self.admin
    Pool(self.pool_addresses[pool_id][token]).remove_liquidity(amount, recipient)
    log RemoveLiquidity(pool_id, amount, recipient)

@external
def withdraw_fee(pool_id: uint256, token: address, amount: uint256):
    assert msg.sender == self.admin
    Pool(self.pool_addresses[pool_id][token]).remove_liquidity(amount, GOVERNANCE)
    log FeeWithdrawn(pool_id, amount, GOVERNANCE)
