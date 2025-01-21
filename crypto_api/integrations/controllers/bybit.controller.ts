import { Controller, Get, Req, UseGuards } from '@nestjs/common';
import { IntegrationsService } from '../services/integration.service';
import { AuthGuard } from 'src/auth/auth.guard';
import { ByBitService } from '../services/bybit.service';

@UseGuards(AuthGuard)
@Controller('bybit')
export class ByBitController {
  constructor(
    private readonly byBit: ByBitService,
    private readonly integrationsService: IntegrationsService,
  ) {}

  @Get('account')
  async getAccountInfo(@Req() req: any) {
    const userId = req.user.userId;

    // Get ByBit integration data for the user
    const integration = await this.integrationsService.getUserIntegrations(userId);
    const byBitIntegration = integration.find((i) => i.platform === 'bybit');
    if (!byBitIntegration) {
      throw new Error('ByBit integration not found');
    }

    // Get API Key and Secret Key for ByBit integration
    const { apiKey, secretKey } = byBitIntegration; // Use API keys
    return this.byBit.getAccountInfo(apiKey, secretKey);
  }

}
