# Sample Data: OpenWeatherMap — *Deprecated*

Deprecated Feature

The sample weather data has been deprecated and may not be available in some regions.

[OpenWeatherMap](http://openweathermap.org/) is a repository of recent historical and forecasted weather data in JSON format. Snowflake imports this
weather data and makes it available to all Snowflake accounts free of charge so you can experiment with our unique, high-performance semi-structured
columnar functionality using real-world data.

Important

The sample weather data is provided for evaluation and testing purposes. The data is updated regularly in Snowflake, but is not maintained in real-time,
which may result in occasional lapses in updates (i.e. we do not guarantee that the data is always current and/or gap-free).

As such, we do not recommend using the data in production systems.

## Tables

The data set includes the following tables, all stored in native JSON format and accumulated over time:

| Table Name | Description | JSON Description |
| --- | --- | --- |
| DAILY\_14\_TOTAL | 12 days of daily weather forecasts for 20,000+ cities. | Click [here](http://openweathermap.org/forecast16#JSON) |
| DAILY\_16\_TOTAL | 12 days of daily weather forecasts for 200,000+ cities (lower frequency of updates). | Click [here](http://openweathermap.org/forecast16#JSON) |
| HOURLY\_14\_TOTAL | 4 days of hourly weather forecasts for 20,000+ cities. | Click [here](http://openweathermap.org/forecast5#JSON) |
| HOURLY\_16\_TOTAL | 4 days of hourly weather forecasts for 200,000+ cities (lower frequency of updates). | Click [here](http://openweathermap.org/forecast5#JSON) |
| WEATHER\_14\_TOTAL | Recent weather for 20,000 cities. | Click [here](http://openweathermap.org/current#current_JSON) |

Expand

Show lessSee more

## Query Examples

The following query retrieves the recent high and low temperature readings for New York City, converted from celsius to fahrenheit temperatures, along with the latitude and longitude for
the readings:

> Copy code
>
> ```
> select (V:main.temp_max - 273.15) * 1.8000 + 32.00 as temp_max_far,
>        (V:main.temp_min - 273.15) * 1.8000 + 32.00 as temp_min_far,
>        cast(V:time as TIMESTAMP) time,
>        V:city.coord.lat lat,
>        V:city.coord.lon lon,
>        V
> from snowflake_sample_data.weather.WEATHER_14_TOTAL
> where v:city.name = 'New York'
> and   v:city.country = 'US'
> order by time desc
> limit 10;
> ```

The following query compares weather forecasts to actual weather readings:

> Copy code
>
> ```
> with
> forecast as
> (select ow.V:time         as prediction_dt,
>         ow.V:city.name    as city,
>         ow.V:city.country as country,
>         cast(f.value:dt   as timestamp) as forecast_dt,
>         f.value:temp.max  as forecast_max_k,
>         f.value:temp.min  as forecast_min_k,
>         f.value           as forecast
>  from snowflake_sample_data.weather.daily_16_total ow, lateral FLATTEN(input => V, path => 'data') f),
>
> actual as
> (select V:main.temp_max as temp_max_k,
>         V:main.temp_min as temp_min_k,
>         cast(V:time as timestamp)     as time_dt,
>         V:city.name     as city,
>         V:city.country  as country
>  from snowflake_sample_data.weather.WEATHER_14_TOTAL)
>
> select cast(forecast.prediction_dt as timestamp) prediction_dt,
>        forecast.forecast_dt,
>        forecast.forecast_max_k,
>        forecast.forecast_min_k,
>        actual.temp_max_k,
>        actual.temp_min_k
> from actual
> left join forecast on actual.city = forecast.city and
>                       actual.country = forecast.country and
>                       date_trunc(day, actual.time_dt) = date_trunc(day, forecast.forecast_dt)
> where actual.city = 'New York'
> and   actual.country = 'US'
> order by forecast_dt desc, prediction_dt desc;
> ```
