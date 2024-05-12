import React, { useState, useEffect } from "react";
import axios from "axios";
import { Text, View, StyleSheet } from "react-native";

const District = ({ latitude, longitude, onDistrictChange }) => {
  const [district, setDistrict] = useState(null);

  useEffect(() => {
    const reverseGeocode = async () => {
      try {
        const response = await axios.get(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
        );
        if (response.data.address) {
          const district =
            response.data.address.suburb ||
            response.data.address.county ||
            "District not found";
          setDistrict(district);
          onDistrictChange(district);
        } else {
          setDistrict("District not found");
        }
      } catch (error) {
        console.error("Error fetching district:", error);
        setDistrict("District not found");
      }
    };

    if (latitude && longitude) {
      reverseGeocode();
    }
  }, [latitude, longitude]);

  return (
    <View>
      {district ? (
        <Text style={styles.text}>District: {district}</Text>
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

export default District;
