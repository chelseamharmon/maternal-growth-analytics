INSERT INTO dim_acquisition_channel (channel_name, channel_type)
VALUES
  ('paid_search', 'paid'),
  ('paid_social', 'paid'),
  ('ob_referral', 'referral'),
  ('employer', 'partnership'),
  ('organic', 'organic'),
  ('partner_clinic', 'partnership')
ON CONFLICT (channel_name) DO NOTHING;

