import React, { useState, useEffect } from "react";
import axios from "axios";
import { Text, View, StyleSheet } from "react-native";
import moment from "moment"; // Import moment

const Weather = ({ district, lat, long }) => {
  const [weather, setWeather] = useState(null);
  const currentDate = new Date();

  // Calculate 1 year ago date
  const oneYearAgoDate = new Date(currentDate);
  oneYearAgoDate.setFullYear(currentDate.getFullYear() - 1);

  // Calculate 6 months later date from 1 year ago date
  const sixMonthsLaterDate = new Date(oneYearAgoDate);
  sixMonthsLaterDate.setMonth(oneYearAgoDate.getMonth() + 7);

  // Format dates to YYYY-MM-DD
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };
  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const response = await axios.get(
          `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${lat}%2C${long}/${formatDate(
            oneYearAgoDate
          )}/${formatDate(
            sixMonthsLaterDate
          )}?unitGroup=metric&include=days&key=WC52MYN72HBTF6FETJ9JD4K8N&contentType=json`
        );
        console.log(currentDate);
        console.log(formatDate(oneYearAgoDate));
        console.log(formatDate(sixMonthsLaterDate));
        console.log(response.data.days.length);
        setWeather(response.data.days);
      } catch (error) {
        console.error("Error fetching weather data:", error);
        setWeather(null);
      }
    };

    if (district) {
      fetchWeatherData();
    }
  }, [district]);

  return (
    <View>
      {weather ? (
        <View>
          <Text style={styles.text}> Weather fetched</Text>
          {/* <Text>Temperature: {weather.main.temp}°C</Text>
          <Text>Description: {weather.weather[0].description}</Text> */}
        </View>
      ) : (
        <Text>Loading...</Text>
      )}
    </View>
  );
};
const styles = StyleSheet.create({
  text: {
    fontSize: 25,
  },
});

export default Weather;
