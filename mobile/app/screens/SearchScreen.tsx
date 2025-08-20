import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, TextInput, Button, Card, Chip } from 'react-native-paper';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../App';
import { config } from '../utils/config';

type SearchScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Search'>;

interface Props {
  navigation: SearchScreenNavigationProp;
}

const SearchScreen: React.FC<Props> = ({ navigation }) => {
  const [originPort, setOriginPort] = useState('');
  const [destPort, setDestPort] = useState('');
  const [date, setDate] = useState('');
  const [pax, setPax] = useState('1');

  const popularPorts = ['Split', 'Hvar', 'Vis', 'Korčula', 'Dubrovnik', 'Zadar'];

  const handleSearch = () => {
    if (originPort && destPort && date && pax) {
      navigation.navigate('Results', {
        originPort,
        destPort,
        date,
        pax: parseInt(pax),
      });
    }
  };

  const selectPort = (port: string, isOrigin: boolean) => {
    if (isOrigin) {
      setOriginPort(port);
    } else {
      setDestPort(port);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge" style={styles.title}>
            Search Routes
          </Text>
          
          <TextInput
            label="From Port"
            value={originPort}
            onChangeText={setOriginPort}
            style={styles.input}
            mode="outlined"
          />

          <TextInput
            label="To Port"
            value={destPort}
            onChangeText={setDestPort}
            style={styles.input}
            mode="outlined"
          />

          <TextInput
            label="Date (YYYY-MM-DD)"
            value={date}
            onChangeText={setDate}
            style={styles.input}
            mode="outlined"
            placeholder="2024-08-15"
          />

          <TextInput
            label="Passengers"
            value={pax}
            onChangeText={setPax}
            style={styles.input}
            mode="outlined"
            keyboardType="numeric"
          />

          <Button
            mode="contained"
            onPress={handleSearch}
            style={styles.searchButton}
            disabled={!originPort || !destPort || !date || !pax}
          >
            Search Routes
          </Button>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.subtitle}>
            Popular Ports
          </Text>
          <View style={styles.chipContainer}>
            {popularPorts.map((port) => (
              <View key={port} style={styles.chipRow}>
                <Chip
                  mode="outlined"
                  onPress={() => selectPort(port, true)}
                  style={[styles.chip, originPort === port && styles.selectedChip]}
                >
                  From {port}
                </Chip>
                <Chip
                  mode="outlined"
                  onPress={() => selectPort(port, false)}
                  style={[styles.chip, destPort === port && styles.selectedChip]}
                >
                  To {port}
                </Chip>
              </View>
            ))}
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  card: {
    marginBottom: 20,
    elevation: 4,
  },
  title: {
    marginBottom: 20,
    color: '#333',
    textAlign: 'center',
  },
  subtitle: {
    marginBottom: 15,
    color: '#333',
  },
  input: {
    marginBottom: 15,
  },
  searchButton: {
    backgroundColor: '#667eea',
    marginTop: 10,
  },
  chipContainer: {
    marginTop: 10,
  },
  chipRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  chip: {
    flex: 1,
    marginHorizontal: 5,
  },
  selectedChip: {
    backgroundColor: '#667eea',
  },
});

export default SearchScreen; 