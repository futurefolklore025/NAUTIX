import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Card, Button } from 'react-native-paper';
import { StackNavigationProp } from '@react-navigation/stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';

type ResultsScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Results'>;
type ResultsScreenRouteProp = RouteProp<RootStackParamList, 'Results'>;

interface Props {
  navigation: ResultsScreenNavigationProp;
  route: ResultsScreenRouteProp;
}

const ResultsScreen: React.FC<Props> = ({ navigation, route }) => {
  const { originPort, destPort, date, pax } = route.params;

  // Mock data - in real app, this would come from API
  const mockSchedules = [
    {
      id: '1',
      departureTime: '08:00',
      arrivalTime: '09:30',
      operator: 'Jadrolinija',
      price: 15,
      capacity: 200,
    },
    {
      id: '2',
      departureTime: '16:00',
      arrivalTime: '17:30',
      operator: 'Kapetan Luka',
      price: 18,
      capacity: 150,
    },
  ];

  const handleBooking = (scheduleId: string) => {
    // In real app, this would create a booking and navigate to ticket
    navigation.navigate('Ticket', {
      bookingId: 'mock-booking-123',
      ticketId: 'mock-ticket-456',
    });
  };

  return (
    <View style={styles.container}>
      <Card style={styles.summaryCard}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.summaryTitle}>
            Search Results
          </Text>
          <Text variant="bodyMedium">
            {originPort} → {destPort}
          </Text>
          <Text variant="bodyMedium">Date: {date}</Text>
          <Text variant="bodyMedium">Passengers: {pax}</Text>
        </Card.Content>
      </Card>

      {mockSchedules.map((schedule) => (
        <Card key={schedule.id} style={styles.scheduleCard}>
          <Card.Content>
            <View style={styles.scheduleHeader}>
              <Text variant="titleMedium">{schedule.operator}</Text>
              <Text variant="titleLarge" style={styles.price}>
                €{schedule.price}
              </Text>
            </View>
            
            <View style={styles.scheduleDetails}>
              <View style={styles.timeContainer}>
                <Text variant="bodyLarge">{schedule.departureTime}</Text>
                <Text variant="bodySmall">Departure</Text>
              </View>
              
              <View style={styles.timeContainer}>
                <Text variant="bodyLarge">{schedule.arrivalTime}</Text>
                <Text variant="bodySmall">Arrival</Text>
              </View>
              
              <View style={styles.capacityContainer}>
                <Text variant="bodyMedium">Capacity: {schedule.capacity}</Text>
              </View>
            </View>
          </Card.Content>
          
          <Card.Actions>
            <Button
              mode="contained"
              onPress={() => handleBooking(schedule.id)}
              style={styles.bookButton}
            >
              Book Now
            </Button>
          </Card.Actions>
        </Card>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  summaryCard: {
    marginBottom: 20,
    elevation: 4,
  },
  summaryTitle: {
    marginBottom: 15,
    color: '#333',
    fontWeight: 'bold',
  },
  scheduleCard: {
    marginBottom: 15,
    elevation: 4,
  },
  scheduleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  price: {
    color: '#667eea',
    fontWeight: 'bold',
  },
  scheduleDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  timeContainer: {
    alignItems: 'center',
  },
  capacityContainer: {
    alignItems: 'center',
  },
  bookButton: {
    backgroundColor: '#667eea',
  },
});

export default ResultsScreen; 