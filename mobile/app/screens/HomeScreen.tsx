import React from 'react';
import { View, StyleSheet, Image } from 'react-native';
import { Text, Button, Card } from 'react-native-paper';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../App';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

interface Props {
  navigation: HomeScreenNavigationProp;
}

const HomeScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text variant="displaySmall" style={styles.title}>
          🌊 Welcome to Nautix
        </Text>
        <Text variant="bodyLarge" style={styles.subtitle}>
          Your maritime travel companion
        </Text>
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            Find Your Perfect Route
          </Text>
          <Text variant="bodyMedium" style={styles.cardText}>
            Search for ferries, charters, and boat rentals across the Mediterranean
          </Text>
        </Card.Content>
        <Card.Actions>
          <Button 
            mode="contained" 
            onPress={() => navigation.navigate('Search')}
            style={styles.searchButton}
          >
            Search Routes
          </Button>
        </Card.Actions>
      </Card>

      <View style={styles.features}>
        <Text variant="titleMedium" style={styles.featuresTitle}>
          What Nautix Offers:
        </Text>
        <View style={styles.featureItem}>
          <Text variant="bodyMedium">🚢 Ferry schedules & booking</Text>
        </View>
        <View style={styles.featureItem}>
          <Text variant="bodyMedium">⛵ Private charters & rentals</Text>
        </View>
        <View style={styles.featureItem}>
          <Text variant="bodyMedium">📱 Digital tickets & QR codes</Text>
        </View>
        <View style={styles.featureItem}>
          <Text variant="bodyMedium">📍 Real-time tracking</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 40,
  },
  title: {
    textAlign: 'center',
    color: '#667eea',
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    textAlign: 'center',
    color: '#666',
  },
  card: {
    marginBottom: 30,
    elevation: 4,
  },
  cardTitle: {
    marginBottom: 10,
    color: '#333',
  },
  cardText: {
    marginBottom: 20,
    color: '#666',
  },
  searchButton: {
    backgroundColor: '#667eea',
    marginTop: 10,
  },
  features: {
    flex: 1,
  },
  featuresTitle: {
    marginBottom: 20,
    color: '#333',
    fontWeight: 'bold',
  },
  featureItem: {
    marginBottom: 15,
    paddingLeft: 10,
  },
});

export default HomeScreen; 