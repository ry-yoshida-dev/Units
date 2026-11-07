# Quantities

Arithmetic between quantities in the `units.quantity` package.

| Operation | Result |
|-----------|--------|
| `Length * Length` | `Area` in square meters |
| `Length * Area`, `Area * Length` | `Volume` in cubic meters |
| `Area / Length` | `Length` in meters |
| `Volume / Area` | `Length` in meters |
| `Volume / Length` | `Area` in square meters |
| `Length / Time` | `Speed` in meters per second |
| `Length / Speed` | `Time` in seconds |
| `Speed * Time`, `Time * Speed` | `Length` in meters |
| `Speed / Frequency` | `Length` in meters (the wavelength) |
| `Speed / Length` | `Frequency` in hertz |
| `Length * Frequency`, `Frequency * Length` | `Speed` in meters per second |
| `Frequency * Time`, `Time * Frequency` | `NumericArray` (the number of cycles) |

Arithmetic between quantities that is not listed here raises `TypeError`.
