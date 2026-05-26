import React, { useState } from 'react';
import { View, Text, Button, Alert, ActivityIndicator, TextInput, StyleSheet } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';
import { generateVideo, getJobStatus } from '../api/client';

export default function HomeScreen({ navigation }) {
  const [audio, setAudio] = useState(null);
  const [image, setImage] = useState(null);
  const [musicUrl, setMusicUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);

  const pickAudio = async () => {
    const result = await DocumentPicker.getDocumentAsync({ type: 'audio/*' });
    if (result.assets) setAudio(result.assets[0]);
  };

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: 'images' });
    if (!result.canceled) setImage(result.assets[0]);
  };

  const handleGenerate = async () => {
    if (!audio && !musicUrl) return Alert.alert('Error', 'Please provide audio file or URL');
    if (!image) return Alert.alert('Error', 'Please select a source image');

    setLoading(true);
    try {
      const id = await generateVideo(audio, image, musicUrl);
      setJobId(id);
      pollStatus(id);
    } catch (err) {
      Alert.alert('Error', err.message);
      setLoading(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      const statusData = await getJobStatus(id);
      if (statusData.status === 'completed') {
        clearInterval(interval);
        setLoading(false);
        navigation.navigate('Player', { videoUrl: statusData.video_url });
      } else if (statusData.status === 'failed') {
        clearInterval(interval);
        setLoading(false);
        Alert.alert('Failed', statusData.error);
      }
    }, 2000);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Music Video Generator</Text>
      <Button title="Pick Audio File" onPress={pickAudio} />
      {audio && <Text>Audio: {audio.name}</Text>}
      <TextInput
        style={styles.input}
        placeholder="Or paste Suno/aimusic.so link"
        value={musicUrl}
        onChangeText={setMusicUrl}
      />
      <Button title="Pick Source Image" onPress={pickImage} />
      {image && <Text>Image: {image.fileName}</Text>}
      <Button title="Generate Video" onPress={handleGenerate} disabled={loading} />
      {loading && <ActivityIndicator size="large" />}
      {jobId && <Text>Processing... Job ID: {jobId}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginVertical: 10, borderRadius: 5 }
});
