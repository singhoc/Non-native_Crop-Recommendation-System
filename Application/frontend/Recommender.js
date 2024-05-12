import React from "react";
import { Text, View, Button, Modal } from "react-native";

const Recommender = ({
  visible,
  onClose,
  predictedCrop,
  benefits,
  timetogrow,
  profitmargin,
  costperkg,
}) => {
  return (
    <Modal
      style={{ backgroundColor: "black" }}
      visible={visible}
      animationType="slide"
      onRequestClose={onClose}
    >
      <View style={{ flex: 1, padding: 10, margin: 50 }}>
        <Text style={{ fontSize: 15, fontWeight: "bold", marginBottom: 10 }}>
          Recommended Crop:
        </Text>
        <Text style={{ fontSize: 12, marginBottom: 20 }}>{predictedCrop}</Text>
        <Text style={{ fontSize: 15, fontWeight: "bold", marginBottom: 10 }}>
          About Crop:
        </Text>
        <Text style={{ fontSize: 12, marginBottom: 25 }}>{benefits}</Text>
        <Text style={{ fontSize: 15, fontWeight: "bold", marginBottom: 10 }}>
          Estimated Cost Per Kg in Market:
        </Text>
        <Text style={{ fontSize: 12, marginBottom: 25 }}>{costperkg}</Text>
        <Text style={{ fontSize: 15, fontWeight: "bold", marginBottom: 10 }}>
          Profit Margin:
        </Text>
        <Text style={{ fontSize: 12, marginBottom: 25 }}>{profitmargin}</Text>
        <Text style={{ fontSize: 15, fontWeight: "bold", marginBottom: 10 }}>
          Time To Grow:
        </Text>
        <Text style={{ fontSize: 12, marginBottom: 25 }}>{timetogrow}</Text>
        <Button title="Close" onPress={onClose} />
      </View>
    </Modal>
  );
};

export default Recommender;
