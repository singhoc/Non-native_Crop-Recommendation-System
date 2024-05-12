import React, { useEffect, useState } from "react";
import { Text, View, StyleSheet, ImageBackground, Button } from "react-native";
import Location from "./Location";
import District from "./District";
import Weather from "./Weather";
import Recommender from "./Recommender";
import axios from "axios";

const App = () => {
  const [location, setLocation] = React.useState(null);
  const [district, setDistrict] = React.useState(null);
  const [recommenderVisible, setRecommenderVisible] = useState(false);
  const [predictedCrop, setPredictedCrop] = useState("");
  const [benefits, setBenefits] = useState("");
  const [costPerKg, setCostPerKg] = useState("");
  const [profitMargin, setProfitMargin] = useState("");
  const [timeToGrow, setTimeToGrow] = useState("");

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
          `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${
            location?.coords.latitude
          }%2C${location?.coords.longitude}/${formatDate(
            oneYearAgoDate
          )}/${formatDate(
            sixMonthsLaterDate
          )}?unitGroup=metric&include=days&key=DDFXCLKA7RNEKS9GGPULM6NU2&contentType=json`
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
  const handleRecommendation = async () => {
    // Here you can add your logic to get the predicted crop and its benefits
    // For example, you can make an API call to a server that provides this information
    // For now, we will just set some dummy data
    try {
      // Make the POST request to get the predicted crop
      const response = await axios.post(
        "https://13b8-2409-40d1-a-43a8-c3f1-52a1-9193-7ee4.ngrok-free.app/predict",
        weather
      );

      // Assuming the response contains the predicted crop and its benefits
      const { predicted_category, details } = response.data;

      // Update the state with the predicted crop and benefits
      setPredictedCrop(predicted_category);
      setBenefits(details[0].benefits);
      setCostPerKg(details[0].estimated_cost_per_kg);
      setProfitMargin(details[0].profit_margin);
      setTimeToGrow(details[0].time_to_grow);
      setRecommenderVisible(true);
    } catch (error) {
      console.error("Error fetching predicted crop:", error);
      // Handle errors here
      // For example, you can set default values for predictedCrop and benefits
      setPredictedCrop("Unknown");
      setBenefits("Could not fetch benefits");
      // Optionally, you can also show a user-friendly error message
      // or perform any other error handling logic here
    }
  };
  return (
    <ImageBackground
      source={require("./background.jpg")} // Replace 'background.jpg' with your image file
      style={styles.background}
    >
      <View style={styles.container}>
        <Text style={styles.appName}>Krishi Kalyan</Text>
        <Location onLocationChange={setLocation} />
        <District
          latitude={location?.coords.latitude}
          longitude={location?.coords.longitude}
          onDistrictChange={setDistrict}
        />
        <View style={styles.spacing} />
        <Button title="Ask Recommendation" onPress={handleRecommendation} />
        <Recommender
          visible={recommenderVisible}
          onClose={() => setRecommenderVisible(false)}
          predictedCrop={predictedCrop}
          benefits={benefits}
          timetogrow={timeToGrow}
          profitmargin={profitMargin}
          costperkg={costPerKg}
        />
      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1,
    resizeMode: "cover", // or 'stretch' or 'contain'
    justifyContent: "center",
  },
  container: {
    justifyContent: "center",
    alignItems: "center",
  },
  spacing: {
    margin: 20,
  },
  appName: {
    fontSize: 50,
    fontWeight: "bold",
    color: "black", // Example color (orange-red)
    marginBottom: 300,
  },
});

export default App;
