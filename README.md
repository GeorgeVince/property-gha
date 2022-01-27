# Property Estimate Github Action

This action will update the README with an image of the Zoopla property estimate of a house.

## Inputs

### `property-uprn`

**Required** The property uprn found on Zoopla.  e.g. https://www.zoopla.co.uk/property/uprn/123456/ the uprn would be `123456`

## Outputs

### `out.png`

Updated with todays property price

## Example usage

```yaml
uses: actions/property-gha@master
with:
  property-uprn: '123456'
```