-- 01_supplies.sql

INSERT INTO public.supplies (
  id,
  name,
  category,
  unit,
  cost_per_unit,
  stock_quantity,
  min_stock,
  created_at,
  updated_at
) VALUES
  (
    '11111111-1111-1111-1111-111111111111',
    'Farinha de trigo',
    'Ingredientes',
    'kg',
    3.50,
    20.500,
    5.000,
    NOW(),
    NOW()
  ),
  (
    '22222222-2222-2222-2222-222222222222',
    'Óleo vegetal',
    'Ingredientes',
    'l',
    5.90,
    10.000,
    3.000,
    NOW(),
    NOW()
  ),
  (
    '33333333-3333-3333-3333-333333333333',
    'Saco plástico 20x30',
    'Embalagens',
    'un',
    0.12,
    200,
    50,
    NOW(),
    NOW()
  );