package main

import (
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/labstack/echo"
)

type WeatherData struct {
    Temperature float64 `json:"temperature"`
    Description string  `json:"description"`
    Humidity    int     `json:"humidity"`
    WindSpeed   float64 `json:"wind_speed"`
    Pressure    int     `json:"pressure"`
    Cloudiness  int     `json:"cloudiness"`
    Sunrise     int     `json:"sunrise"`
    Sunset      int     `json:"sunset"`
}

func main() {
    e := echo.New()

    e.GET("/weather", func(c echo.Context) error {
        apiKey := "2419a19fca571a8bc7b672f1ad3c52ed"
        city := c.QueryParam("city") 
        url := fmt.Sprintf("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s", city, apiKey)
        response, err := http.Get(url)
        if err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to get weather data"})
        }
        defer response.Body.Close()

        var weatherData struct {
            Main struct {
                Temp     float64 `json:"temp"`
                Humidity int     `json:"humidity"`
                Pressure int     `json:"pressure"`
            } `json:"main"`
            Weather []struct {
                Description string `json:"description"`
            } `json:"weather"`
            Wind struct {
                Speed float64 `json:"speed"`
            } `json:"wind"`
            Clouds struct {
                All int `json:"all"`
            } `json:"clouds"`
            Sys struct {
                Sunrise int `json:"sunrise"`
                Sunset  int `json:"sunset"`
            } `json:"sys"`
        }
        if err := json.NewDecoder(response.Body).Decode(&weatherData); err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Failed to decode weather data"})
        }

        temperatureCelsius := weatherData.Main.Temp - 273.15
        weather := WeatherData{
            Temperature: temperatureCelsius,
            Description: weatherData.Weather[0].Description,
            Humidity:    weatherData.Main.Humidity,
            WindSpeed:   weatherData.Wind.Speed,
            Pressure:    weatherData.Main.Pressure,
            Cloudiness:  weatherData.Clouds.All,
            Sunrise:     weatherData.Sys.Sunrise,
            Sunset:      weatherData.Sys.Sunset,
        }
        return c.JSON(http.StatusOK, weather)
    })

    e.Logger.Fatal(e.Start(":8080"))
}
