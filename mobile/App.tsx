import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';

import HomeScreen from './app/screens/HomeScreen';
import SearchScreen from './app/screens/SearchScreen';
import ResultsScreen from './app/screens/ResultsScreen';
import TicketScreen from './app/screens/TicketScreen';
import { theme } from './app/utils/theme';

export type RootStackParamList = {
  Home: undefined;
  Search: undefined;
  Results: {
    originPort: string;
    destPort: string;
    date: string;
    pax: number;
  };
  Ticket: {
    bookingId: string;
    ticketId: string;
  };
};

const Stack = createStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: theme.colors.primary,
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Home" 
            component={HomeScreen} 
            options={{ title: 'Nautix' }}
          />
          <Stack.Screen 
            name="Search" 
            component={SearchScreen} 
            options={{ title: 'Search Routes' }}
          />
          <Stack.Screen 
            name="Results" 
            component={ResultsScreen} 
            options={{ title: 'Available Routes' }}
          />
          <Stack.Screen 
            name="Ticket" 
            component={TicketScreen} 
            options={{ title: 'Your Ticket' }}
          />
        </Stack.Navigator>
        <StatusBar style="auto" />
      </NavigationContainer>
    </PaperProvider>
  );
} 