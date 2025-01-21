import { IsNotEmpty, IsString, IsIn } from 'class-validator';

export class LinkPlatformDto {
  @IsString()
  @IsNotEmpty()
  @IsIn(['binance', 'bybit', 'interactiveBrokers'])
  platform: string; // Platform (Binance, Bybit, Interactive Brokers)

  @IsString()
  @IsNotEmpty()
  apiKey: string; // AccessToken

  @IsString()
  secretKey?: string;
}
