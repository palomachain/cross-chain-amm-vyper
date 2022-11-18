def test_add_liquidity(Factory, Compass_EVM, project, alice, ERC20):
    pool_id = 0
    amount = 10 ** 16
    recipient = "recipient"
    Factory.create_pool(ERC20, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, ERC20)
    pool = project.erc20_pool.at(pool_address)
    ERC20.approve(pool, amount, sender=alice)
    tx = pool.add_liquidity(amount, recipient, sender=alice)
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].pool_id == pool_id
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].token == ERC20
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].amount == amount
    assert list(tx.decode_logs(Factory.AddLiquidity))[
        0].depositor == alice.address
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].recipient == recipient


def test_remove_liquidity(Factory, Compass_EVM, project, alice, ERC20):
    pool_id = 0
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(ERC20, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, ERC20)
    pool = project.erc20_pool.at(pool_address)
    ERC20.approve(pool, amount0, sender=alice)
    pool.add_liquidity(amount0, recipient, sender=alice)
    init_bal = ERC20.balanceOf(alice)
    Factory.remove_liquidity(pool_id, ERC20, amount1,
                             alice.address, sender=Compass_EVM)
    assert ERC20.balanceOf(alice) == init_bal + amount1


def test_swap_in(Factory, Compass_EVM, project, alice, ERC20):
    pool_id = 0
    amount = 10 ** 16
    recipient = "recipient"
    Factory.create_pool(ERC20, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, ERC20)
    pool = project.erc20_pool.at(pool_address)
    ERC20.approve(pool, amount, sender=alice)
    tx = pool.swap_in(amount, recipient, sender=alice)
    assert list(tx.decode_logs(Factory.SwapIn))[0].pool_id == pool_id
    assert list(tx.decode_logs(Factory.SwapIn))[0].token == ERC20
    assert list(tx.decode_logs(Factory.SwapIn))[0].amount == amount
    assert list(tx.decode_logs(Factory.SwapIn))[0].recipient == recipient


def test_swap_out(Factory, Compass_EVM, project, alice, ERC20):
    pool_id = 0
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(ERC20, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, ERC20)
    pool = project.erc20_pool.at(pool_address)
    ERC20.approve(pool, amount0, sender=alice)
    pool.add_liquidity(amount0, recipient, sender=alice)
    init_bal = ERC20.balanceOf(alice)
    Factory.swap_out(pool_id, ERC20, amount1,
                     alice.address, sender=Compass_EVM)
    assert ERC20.balanceOf(alice) == init_bal + amount1


def test_withdraw_fee(Factory, Compass_EVM, project, alice, governance, ERC20):
    pool_id = 0
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(ERC20, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, ERC20)
    pool = project.erc20_pool.at(pool_address)
    ERC20.approve(pool, amount0, sender=alice)
    pool.add_liquidity(amount0, recipient, sender=alice)
    init_bal = ERC20.balanceOf(governance)
    Factory.withdraw_fee(pool_id, ERC20, amount1, sender=Compass_EVM)
    assert ERC20.balanceOf(governance) == init_bal + amount1
