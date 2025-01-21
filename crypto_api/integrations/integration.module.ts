import {  Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { Integration, IntegrationSchema } from './schemas/integration.schema';
import { IntegrationsController } from './controllers/integration.controller';
import { BinanceService } from './services/binance.service';
import { IntegrationsService } from './services/integration.service';
import { BinanceController } from './controllers/binance.controller';
import { AuthModule } from 'src/auth/auth.module';
import { UsersModule } from 'src/users/users.module';
import { ByBitController } from './controllers/bybit.controller';
import { ByBitService } from './services/bybit.service';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: Integration.name, schema: IntegrationSchema }]),
    AuthModule,
    UsersModule
  ],
  controllers: [IntegrationsController, BinanceController, ByBitController], // Add controllers
  providers: [IntegrationsService, BinanceService, ByBitService], // Add platforms
  exports: [IntegrationsService, BinanceService, ByBitService], // Export IntegrationsService for use in other modules
})
export class IntegrationsModule {}
