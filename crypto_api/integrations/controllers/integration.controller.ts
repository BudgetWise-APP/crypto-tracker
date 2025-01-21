import { Controller, Post, Delete, Get, Body, Param, Req, UseGuards } from '@nestjs/common';
import { LinkPlatformDto } from '../dto/link-platform.dto';
import { IntegrationsService } from '../services/integration.service';
import { AuthGuard } from 'src/auth/auth.guard';

@UseGuards(AuthGuard)
@Controller('integrations')
export class IntegrationsController {
  constructor(private readonly integrationsService: IntegrationsService) {}

  @Post('link')
  async linkPlatform(@Body() dto: LinkPlatformDto, @Req() req: any) {
    const userId = req.user.userId; // Get userId from token
    return this.integrationsService.linkPlatform(userId, dto.platform, dto.apiKey, dto.secretKey);
  }

  @Delete('unlink/:platform')
  async unlinkPlatform(@Param('platform') platform: string, @Req() req: any) {
    const userId = req.user.userId;
    await this.integrationsService.unlinkPlatform(userId, platform);
    return { message: `Platform ${platform} unlinked successfully` };
  }

  @Get()
  async getUserIntegrations(@Req() req: any) {
    const userId = req.user.userId;
    return this.integrationsService.getUserIntegrations(userId);
  }
}
