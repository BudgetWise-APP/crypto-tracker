import { Controller, Get, Req, UseGuards } from '@nestjs/common';
import { BinanceService } from '../services/binance.service';
import { IntegrationsService } from '../services/integration.service';
import { AuthGuard } from 'src/auth/auth.guard';

@UseGuards(AuthGuard)
@Controller('binance')
export class BinanceController {
  constructor(
    private readonly binanceService: BinanceService,
    private readonly integrationsService: IntegrationsService,
  ) {}

  @Get('account')
  async getAccountInfo(@Req() req: any) {
    const userId = req.user.userId;

    // Get Binance integration data for the user
    const integration = await this.integrationsService.getUserIntegrations(userId);
    const binanceIntegration = integration.find((i) => i.platform === 'binance');
    if (!binanceIntegration) {
      throw new Error('Binance integration not found');
    }

    // Get API Key and Secret Key for Binance integration
    const { apiKey, secretKey } = binanceIntegration; // Use API keys
    return this.binanceService.getAccountInfo(apiKey, secretKey);
  }
}
