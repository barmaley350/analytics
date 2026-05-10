import numpy as np

def geometric_brownian_motion(start_price=1000, days=252, mu=0.1, sigma=0.2):
    """
    start_price: начальная цена
    days: количество дней
    mu: годовая доходность (10%)
    sigma: годовая волатильность (20%)
    """
    dt = 1 / days  # временной шаг
    prices = [start_price]

    for _ in range(days):
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * np.random.normal()
        new_price = prices[-1] * np.exp(drift + diffusion)
        prices.append(new_price)

    return prices
