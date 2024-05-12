import React, { useState, useEffect } from "react";
import { Text, View, StyleSheet } from "react-native";
import * as Locationss from "expo-location";

const Location = ({ onLocationChange }) => {
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    (async () => {
      let { status } = await Locationss.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        setErrorMsg("Permission to access location was denied");
        return;
      }

      let location = await Locationss.getCurrentPositionAsync({});
      setLocation(location);
      onLocationChange(location);
    })();
  }, []);

  return (
    <View>
      {errorMsg ? <Text>{errorMsg}</Text> : null}
      {location ? (
        <View>
          <Text style={styles.text}>
            Latitude: {location.coords.latitude.toFixed(6)}
          </Text>
          <Text style={styles.text}>
            Longitude: {location.coords.longitude.toFixed(6)}
          </Text>
        </View>
      ) : (
        <Text>Waiting for location...</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  text: {
    fontSize: 25,
  },
});

export default Location;
