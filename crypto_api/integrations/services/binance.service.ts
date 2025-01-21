import { Injectable } from "@nestjs/common";
import * as crypto from 'crypto';
import * as querystring from 'querystring';

@Injectable()
export class BinanceService {
  private readonly apiUrl = 'https://api.binance.com';

  // Method to get account information
  async getAccountInfo(apiKey: string, secretKey: string): Promise<any> {
    const endpoint = '/api/v3/account';
    const timestamp = Date.now();
    const params = {
      timestamp, // Binance requires timestamp
    };

    // Sign the request
    const query = querystring.stringify(params);
    const signature = this.sign(query, secretKey);

    // Send request to Binance API
    const response = await fetch(`${this.apiUrl}${endpoint}?${query}&signature=${signature}`, {
      method: 'GET',
      headers: {
        'X-MBX-APIKEY': apiKey, // Use API Key
      },
    });

    if (!response.ok) {
      throw new Error(`Binance API error: ${response.statusText}`);
    }

    return response.json(); // Return JSON response
  }

  async getTotalBalanceInUSD(apiKey: string, secretKey: string): Promise<number> {
    const accountBalances = await this.getAccountInfo(apiKey, secretKey);

    const prices = await this.getPrices();

    const totalInUSD = accountBalances.balances.reduce((total, asset) => {
      const symbol = `${asset.asset}USDT`;
      const price = prices[symbol] || '0';
      return total + parseFloat(asset.free) * parseFloat(price);
    }, 0);

    return totalInUSD;
  }

    private async getPrices(): Promise<Record<string, string>> {
      const endpoint = '/api/v3/ticker/price';
  
      const response = await fetch(`${this.apiUrl}${endpoint}`);
      if (!response.ok) {
        throw new Error(`Binance Prices API error: ${response.statusText}`);
      }
  
      const prices = await response.json();
  
      return prices.reduce((acc, price) => {
        acc[price.symbol] = price.price;
        return acc;
      }, {});
    }

    // Method to sign the request
    private sign(query: string, secretKey: string): string {
      return crypto
        .createHmac('sha256', secretKey)
        .update(query)
        .digest('hex');
    }
}
