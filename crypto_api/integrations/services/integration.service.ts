import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Integration, IntegrationDocument } from '../schemas/integration.schema';

@Injectable()
export class IntegrationsService {
  constructor(
    @InjectModel(Integration.name) private integrationModel: Model<IntegrationDocument>,
  ) {}

  async linkPlatform(userId: string, platform: string, apiKey: string, secretKey?: string): Promise<Integration> {
    const existing = await this.integrationModel.findOne({ userId, platform });
    if (existing) {
      existing.apiKey = apiKey;
      if (secretKey) existing.secretKey = secretKey;
      return existing.save();
    }

    const integration = new this.integrationModel({ userId, platform, apiKey, secretKey });
    return integration.save();
  }

  async unlinkPlatform(userId: string, platform: string): Promise<void> {
    await this.integrationModel.deleteOne({ userId, platform });
  }

  async getUserIntegrations(userId: string): Promise<Integration[]> {
    return this.integrationModel.find({ userId }).exec();
  }
}
