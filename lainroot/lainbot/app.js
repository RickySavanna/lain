// App.js

import React, { useState } from 'react';
import { SafeAreaView, StyleSheet, TextInput, TouchableOpacity, Text, View } from 'react-native';

export default function App() {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    const response = await fetch('http://your-flask-api-url/api/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: userInput }),
    });

    const data = await response.json();
    setChatHistory([...chatHistory, { message: userInput, isUser: true }, { message: data.response, isUser: false }]);
    setUserInput('');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.chatContainer}>
        {chatHistory.map((item, index) => (
          <Text key={index} style={item.isUser ? styles.userMessage : styles.botMessage}>{item.message}</Text>
        ))}
      </View>
      <TextInput style={styles.input} value={userInput} onChangeText={setUserInput} />
      <TouchableOpacity style={styles.button} onPress={sendMessage}>
        <Text style={styles.buttonText}>Send</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingHorizontal: 20 },
  chatContainer: { flex: 1, marginTop: 20 },
  input: { borderColor: 'gray', borderWidth: 1, height: 40, paddingHorizontal: 10 },
  button: { backgroundColor: 'blue', alignItems: 'center', padding: 10, marginTop: 10 },
  buttonText: { color: 'white' },
  userMessage: { textAlign: 'right', color: 'green', marginBottom: 5 },
  botMessage: { textAlign: 'left', color: 'red', marginBottom: 5 },
});
