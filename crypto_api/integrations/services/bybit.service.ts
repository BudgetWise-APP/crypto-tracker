import { Injectable } from '@nestjs/common';
import axios from 'axios';
import * as crypto from 'crypto';

@Injectable()
export class ByBitService {
  private readonly apiUrl = 'https://api.bybit.com';

   // Method to get account balance information
  async getAccountInfo(apiKey: string, secretKey: string): Promise<any> {
    const endpoint = '/v5/account/wallet-balance';
    const timestamp = Date.now().toString();
    const recvWindow = 20000;
    const queryParams = 'accountType=UNIFIED';

    const originString = `${timestamp}${apiKey}${recvWindow}${queryParams}`;

    // Generate signature using HMAC SHA256
    const signature = crypto
      .createHmac('sha256', secretKey)
      .update(originString)
      .digest('hex');

    try {
      const response = await axios.get(`${this.apiUrl}${endpoint}?${queryParams}`, {
        headers: {
          'X-BAPI-API-KEY': apiKey,
          'X-BAPI-SIGN': signature,
          'X-BAPI-TIMESTAMP': timestamp,
          'X-BAPI-RECV-WINDOW': recvWindow,
        },
      });

      return response.data.result;
    } catch (error) {
      throw new Error(`Error fetching account info from Bybit: ${error.message}`);
    }
  }
}
