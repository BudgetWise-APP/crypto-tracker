import { Schema, Prop, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument, Types } from 'mongoose';

export type IntegrationDocument = HydratedDocument<Integration>;

@Schema()
export class Integration {
  @Prop({ type: Types.ObjectId, ref: 'User', required: true })
  userId: Types.ObjectId; // Coonect integration to user

  @Prop({ required: true, enum: ['binance', 'bybit', 'interactiveBrokers'] })
  platform: string; // Platform (Binance, Bybit, Interactive Brokers)

  @Prop({ required: true })
  apiKey: string; // Token or key

  @Prop()
  secretKey?: string;

  @Prop({ default: Date.now })
  createdAt: Date;
}

export const IntegrationSchema = SchemaFactory.createForClass(Integration);
