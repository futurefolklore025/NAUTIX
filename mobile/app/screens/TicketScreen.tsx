import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button } from 'react-native-paper';
import { StackNavigationProp } from '@react-navigation/stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';

type TicketScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Ticket'>;
type TicketScreenRouteProp = RouteProp<RootStackParamList, 'Ticket'>;

interface Props {
  navigation: TicketScreenNavigationProp;
  route: TicketScreenRouteProp;
}

const TicketScreen: React.FC<Props> = ({ navigation, route }) => {
  const { bookingId, ticketId } = route.params;

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.ticketCard}>
        <Card.Content>
          <Text variant="headlineSmall" style={styles.title}>
            🎫 Your Ticket
          </Text>
          
          <View style={styles.ticketInfo}>
            <View style={styles.infoRow}>
              <Text variant="titleMedium">Booking ID:</Text>
              <Text variant="bodyLarge" style={styles.value}>{bookingId}</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text variant="titleMedium">Ticket ID:</Text>
              <Text variant="bodyLarge" style={styles.value}>{ticketId}</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text variant="titleMedium">Status:</Text>
              <Text variant="bodyLarge" style={styles.status}>Confirmed</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.qrCard}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.qrTitle}>
            QR Code
          </Text>
          <View style={styles.qrPlaceholder}>
            <Text variant="bodyLarge" style={styles.qrText}>
              📱 QR Code will be displayed here
            </Text>
            <Text variant="bodySmall" style={styles.qrNote}>
              Show this to staff when boarding
            </Text>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.instructionsCard}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.instructionsTitle}>
            Boarding Instructions
          </Text>
          <Text variant="bodyMedium" style={styles.instruction}>
            • Arrive at the port 30 minutes before departure
          </Text>
          <Text variant="bodyMedium" style={styles.instruction}>
            • Have your ticket ready on your phone
          </Text>
          <Text variant="bodyMedium" style={styles.instruction}>
            • Present the QR code to staff for scanning
          </Text>
          <Text variant="bodyMedium" style={styles.instruction}>
            • Keep your phone charged and accessible
          </Text>
        </Card.Content>
      </Card>

      <View style={styles.actions}>
        <Button
          mode="outlined"
          onPress={() => navigation.navigate('Home')}
          style={styles.homeButton}
        >
          Back to Home
        </Button>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  ticketCard: {
    marginBottom: 20,
    elevation: 4,
  },
  title: {
    textAlign: 'center',
    marginBottom: 20,
    color: '#667eea',
  },
  ticketInfo: {
    marginTop: 15,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  value: {
    fontFamily: 'monospace',
    fontWeight: 'bold',
  },
  status: {
    color: '#4CAF50',
    fontWeight: 'bold',
  },
  qrCard: {
    marginBottom: 20,
    elevation: 4,
  },
  qrTitle: {
    textAlign: 'center',
    marginBottom: 15,
  },
  qrPlaceholder: {
    alignItems: 'center',
    padding: 40,
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
  },
  qrText: {
    marginBottom: 10,
    textAlign: 'center',
  },
  qrNote: {
    textAlign: 'center',
    color: '#666',
  },
  instructionsCard: {
    marginBottom: 20,
    elevation: 4,
  },
  instructionsTitle: {
    marginBottom: 15,
  },
  instruction: {
    marginBottom: 8,
    paddingLeft: 10,
  },
  actions: {
    alignItems: 'center',
    marginTop: 20,
  },
  homeButton: {
    borderColor: '#667eea',
    borderWidth: 2,
  },
});

export default TicketScreen; 