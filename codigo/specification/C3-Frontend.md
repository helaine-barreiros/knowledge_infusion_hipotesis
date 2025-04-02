# AI-Enhanced Personal Finance Management System - Frontend Components (C3)

## Component Diagram

![Frontend Components Diagram](https://www.plantuml.com/plantuml/png/xLjVRzis47_NluB7ts14jghXXBmOZ8SeDWQk9sMaZOY7ZI8sYw4Ttn5LYOKPWoAZPO1UFtx1lP-VVR-lDPSU_vpCXnRnYr47OJM4PY_7xqznGkXPGO2Qwi1Ag9c76LmKK6CeiGRebXWGZfTYCO69S14qj0MqAK3JZ8t56Qi6TuLImOl_XUc_VfM_YO0K-KwCdv3C5_FH2JKr7Lr9GnJW12mqRh8QXQoLQg8WDP9fSGeCRSCb0X4ww8rMXPIAJOB4uLrvE7fxX65Xr1sRCG4IZQIEb9p8Aoc9jDIuDVdqZKY8XxbJGiACRDY74zw9XVK0rg1vvG9Pu0cQSLcYzSuPQnSdx8rsSzfCBz8sSVndSrC3FRvvvQJm5VnHT7lWNREpqfIyqKcWfEjpQD22_7z3RPUXpXxcsMbZaXqELNnSl0MROpDGmXNgbV06G7LcWjawJH9lCPLdudLnhkqOCxe7YuOQHDVTiilDyDHE0qA9eGnOtZfjxwFb8lLDJ_IJK4KLp7fjLTaRtC_DORQd4BeCJHFWZeaUyHQp0I7pFB5Pl5MrlHmwmRxQsYnY-jCnOL33gQwQxS1MrNQGiJYKRKHRRvxT3CZabQZSN7q2s47p1gZoOOJ_0SJexO4SQGZQKCEkxozwFOd5iMY9lmwXJ4dqXDncHnQXjBvgIbNAFUCWObPL36CX0wk7rJUNjj9Lzaf1_iiS35vFsN6_ynNHHRMRRR6qscJ-8_9zCrwxJcOI5v4dU0JR8FYnS9-VpyfFwsqZlCYcQS-MKnH5FfYVvYzNMB94-sSF7CyoErdcx1N0CjdpE6-w-F9L4c_8T0x4LH6C4_f3eCu9fQgj0BLn05MmBaM7HWw-bGkDKXKt2Qe_yUIPZigtbhBiqzBx-FjhfBKpI0qHXwt2UDZ7Eu_n4jkr0NqrB3S-PgOTGVUOuCIJDLwTjBp2hjTgxwWY9A-k8QnmL4k5uP-xL8hRhCqXB0RwPkzchldTfDqgk9f9gL7z9_qmyLfzU2KF_ks3TGkMWfgL6WZzqtKLDt2FkME1aqpkqMoBzDzjpZLKi_3tJlUlW3Lx4wBKBw46J49tYVNEe_P_ssBBkB-gIcdVTu0iM8QrSBOL1Xmcwqg-FEgzvdD5OiX7YqyzWjsUJ75b1_SaSYchBBBdxdJvZ-1N-rEWVOV-jLLhHRk5D2GS_cJJJmhhT0Yg5MRlzLLgK4Ly3GILcIgQwQSA-QrpxMQYF-EUe5lxZUPWd9zkvfjkKzzZQXHzdx4XQ3UaFBHEAaxLx3_Vy-NJLhmxd8-oGSaJZhM-3KA9jgL5zAQR-rUd4fxR6CsSBgJcfvkTrCx0w-tSs_lPeqRPRsLdU9Vd2eB1xPh3U_Gd7mfhQ3UJ9ZZwcpQ-_g6E_aEy1IZzODh5_u6wxH1JhQMDXL_YE0Vu_-EVJEYDlVXN_fR4UiFzcf-ygFwmPY3l7H67r-qBLq6kFQiQJ_Gp9cEeEDizZ_dNGrW-jLBJJ9uKQMeJF_plzn2QJo-CXLVLWV-Tuj_u5ewtyCTqI_0G)

## Implementation Guidelines for Frontend Developers

This document provides detailed guidelines for developers working on the AI-Enhanced Personal Finance Management System frontend. It outlines the architecture, component structure, conventions, and implementation rules to ensure architectural consistency across the frontend applications.

## 1. Project Structure and Organization

The frontend system consists of three main applications: Web Application, Mobile Application, and Advisor Portal. Each follows a structured organization pattern appropriate for its platform but adheres to shared principles.

### 1.1 Web Application Structure

```
web-app/
├── public/                # Static files
│   ├── index.html
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── assets/            # Images, fonts, etc.
│   ├── components/        # Reusable UI components
│   │   ├── common/        # Generic components
│   │   ├── charts/        # Chart components
│   │   ├── forms/         # Form components
│   │   └── layout/        # Layout components
│   ├── config/            # Configuration files
│   ├── constants/         # Constants and enums
│   ├── features/          # Feature modules
│   │   ├── auth/          # Authentication feature
│   │   ├── dashboard/     # Dashboard feature
│   │   ├── transactions/  # Transactions feature
│   │   ├── budgets/       # Budget feature
│   │   ├── goals/         # Financial goals feature
│   │   └── insights/      # Financial insights feature
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API services
│   ├── store/             # Redux store
│   │   ├── slices/        # Redux slices
│   │   └── index.ts       # Store configuration
│   ├── styles/            # Global styles
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Utility functions
│   ├── App.tsx            # Root component
│   └── index.tsx          # Entry point
├── .eslintrc.js           # ESLint configuration
├── .prettierrc            # Prettier configuration
├── tsconfig.json          # TypeScript configuration
├── package.json           # Dependencies and scripts
└── README.md              # Project documentation
```

### 1.2 Mobile Application Structure

```
mobile-app/
├── assets/                # Images, fonts, etc.
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── common/        # Generic components
│   │   ├── charts/        # Chart components
│   │   ├── forms/         # Form components
│   │   └── layout/        # Layout components
│   ├── config/            # Configuration files
│   ├── constants/         # Constants and enums
│   ├── features/          # Feature modules
│   │   ├── auth/          # Authentication feature
│   │   ├── dashboard/     # Dashboard feature
│   │   ├── transactions/  # Transactions feature
│   │   ├── budgets/       # Budget feature
│   │   ├── goals/         # Financial goals feature
│   │   └── insights/      # Financial insights feature
│   ├── hooks/             # Custom React hooks
│   ├── navigation/        # Navigation configuration
│   ├── services/          # API services
│   ├── store/             # Redux store
│   │   ├── slices/        # Redux slices
│   │   └── index.ts       # Store configuration
│   ├── styles/            # Global styles
│   ├── types/             # TypeScript type definitions
│   ├── utils/             # Utility functions
│   ├── App.tsx            # Root component
│   └── index.ts           # Entry point
├── app.json               # Expo configuration
├── babel.config.js        # Babel configuration
├── tsconfig.json          # TypeScript configuration
├── package.json           # Dependencies and scripts
└── README.md              # Project documentation
```

### 1.3 Advisor Portal Structure

Similar to the Web Application structure but with advisor-specific features.

## 2. Layer Architecture and Communication

### 2.1 Frontend Layered Architecture

Each application follows a layered architecture with clear separation of concerns:

1. **Presentation Layer**
   - React components (UI)
   - Layout and styling
   - View-specific logic

2. **Application Layer**
   - Feature modules
   - Routing and navigation
   - State management (Redux)
   - Custom hooks

3. **Domain Layer**
   - Business logic
   - Data transformations
   - Validation rules

4. **Data Access Layer**
   - API client services
   - Local storage services
   - Data caching mechanisms

### 2.2 Layer Communication Rules

The following rules govern communication between layers:

1. **Direction of Dependency**:
   - Higher layers can depend on lower layers, not vice versa
   - UI components → Features → Services → API clients

2. **Data Flow**:
   - One-way data flow preferred (Redux or Context API)
   - Parent-to-child component communication via props
   - Child-to-parent communication via callbacks
   - Component-to-component communication via state management

3. **Feature Isolation**:
   - Features should be isolated from one another
   - Shared state through global state management
   - Cross-feature communication via events or global state

4. **API Communication**:
   - All API calls through service layer
   - Components never directly call APIs
   - Use custom hooks to encapsulate API logic

## 3. Component Design and Implementation

### 3.1 Component Types

#### 3.1.1 Presentational Components

Focused on UI rendering, receive data via props:

```tsx
// Simple presentational component
import React from 'react';
import { styled } from 'styled-components';

interface CardProps {
  title: string;
  children: React.ReactNode;
  variant?: 'default' | 'outlined';
}

const StyledCard = styled.div<{ variant: string }>`
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  background-color: ${props => props.variant === 'outlined' ? 'transparent' : '#ffffff'};
  border: ${props => props.variant === 'outlined' ? '1px solid #e0e0e0' : 'none'};
  box-shadow: ${props => props.variant === 'outlined' ? 'none' : '0 2px 4px rgba(0,0,0,0.1)'};
`;

const CardTitle = styled.h3`
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 500;
`;

export const Card: React.FC<CardProps> = ({ 
  title, 
  children, 
  variant = 'default' 
}) => {
  return (
    <StyledCard variant={variant}>
      {title && <CardTitle>{title}</CardTitle>}
      {children}
    </StyledCard>
  );
};
```

#### 3.1.2 Container Components

Connect to state management and handle business logic:

```tsx
// Container component
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Card } from '../components/Card';
import { TransactionList } from '../components/TransactionList';
import { fetchRecentTransactions } from '../store/slices/transactionsSlice';
import { RootState, AppDispatch } from '../store';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';

export const RecentTransactionsContainer: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { transactions, loading, error } = useSelector(
    (state: RootState) => state.transactions.recent
  );
  
  useEffect(() => {
    dispatch(fetchRecentTransactions());
  }, [dispatch]);
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <Card title="Recent Transactions">
      <TransactionList transactions={transactions} />
    </Card>
  );
};
```

#### 3.1.3 Feature Components

Combine multiple components to implement a complete feature:

```tsx
// Feature component
import React from 'react';
import { styled } from 'styled-components';
import { RecentTransactionsContainer } from './RecentTransactionsContainer';
import { TransactionSummaryContainer } from './TransactionSummaryContainer';
import { TransactionFiltersContainer } from './TransactionFiltersContainer';

const TransactionsPageLayout = styled.div`
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 24px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const Sidebar = styled.div`
  grid-column: 1;
`;

const MainContent = styled.div`
  grid-column: 2;
  
  @media (max-width: 768px) {
    grid-column: 1;
  }
`;

export const TransactionsFeature: React.FC = () => {
  return (
    <TransactionsPageLayout>
      <Sidebar>
        <TransactionFiltersContainer />
        <TransactionSummaryContainer />
      </Sidebar>
      <MainContent>
        <RecentTransactionsContainer />
      </MainContent>
    </TransactionsPageLayout>
  );
};
```

### 3.2 Component Best Practices

1. **Single Responsibility Principle**:
   - Each component should do one thing well
   - Break complex components into smaller ones

2. **Props Design**:
   - Use TypeScript interfaces for prop types
   - Provide default values for optional props
   - Document props with JSDoc comments

3. **Component Composition**:
   - Use composition over inheritance
   - Use children prop for flexible component content
   - Consider render props or higher-order components for complex scenarios

4. **Performance Optimization**:
   - Use React.memo for pure components
   - Use useCallback for callbacks passed to child components
   - Use useMemo for expensive calculations
   - Implement virtualization for long lists

### 3.3 Component Folder Structure

For complex components, use the following structure:

```
Button/
├── Button.tsx            # Main component
├── Button.styles.ts      # Styled components
├── Button.test.tsx       # Unit tests
├── Button.stories.tsx    # Storybook stories
└── index.ts              # Export file
```

## 4. Naming Conventions

### 4.1 File and Folder Naming

1. **Components**:
   - PascalCase for component files: `Button.tsx`, `TransactionList.tsx`
   - PascalCase for component folders: `Button/`, `TransactionList/`

2. **Hooks**:
   - camelCase with 'use' prefix: `useAuth.ts`, `useTransactions.ts`

3. **Utilities**:
   - camelCase: `formatCurrency.ts`, `dateUtils.ts`

4. **Redux Files**:
   - camelCase for slices: `transactionsSlice.ts`, `authSlice.ts`
   - camelCase for action files: `transactionActions.ts`

5. **Constants**:
   - camelCase: `apiEndpoints.ts`, `errorMessages.ts`

6. **Types**:
   - PascalCase with type semantics: `Transaction.types.ts`, `User.types.ts`

### 4.2 Component Naming

1. **Base Components**:
   - Simple, clear nouns: `Button`, `Card`, `Input`

2. **Feature Components**:
   - Descriptive of functionality: `TransactionList`, `BudgetChart`

3. **Container Components**:
   - Add 'Container' suffix: `TransactionListContainer`, `BudgetChartContainer`

4. **Page Components**:
   - Add 'Page' suffix: `DashboardPage`, `TransactionsPage`

5. **HOCs (Higher Order Components)**:
   - Add 'with' prefix: `withAuth`, `withLoading`

### 4.3 CSS / Styled Components Naming

1. **Styled Components**:
   - PascalCase with descriptive names: `StyledButton`, `CardContainer`
   - Add logical prefixes: `StyledHeader`, `StyledFooter`

2. **CSS Classes** (if used):
   - kebab-case: `transaction-item`, `budget-progress-bar`
   - BEM methodology for complex components:
     - Block: `transaction-card`
     - Element: `transaction-card__title`
     - Modifier: `transaction-card--highlighted`

## 5. State Management

### 5.1 Redux Implementation

1. **Store Configuration**:

```tsx
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import authReducer from './slices/authSlice';
import transactionsReducer from './slices/transactionsSlice';
import budgetsReducer from './slices/budgetsSlice';
import goalsReducer from './slices/goalsSlice';
import insightsReducer from './slices/insightsSlice';
import { api } from '../services/api';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    transactions: transactionsReducer,
    budgets: budgetsReducer,
    goals: goalsReducer,
    insights: insightsReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

2. **Redux Toolkit Slice**:

```tsx
// store/slices/transactionsSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { TransactionService } from '../../services/TransactionService';
import { Transaction, TransactionFilters } from '../../types/Transaction.types';

export const fetchTransactions = createAsyncThunk(
  'transactions/fetchTransactions',
  async (filters: TransactionFilters, { rejectWithValue }) => {
    try {
      return await TransactionService.getTransactions(filters);
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  }
);

interface TransactionsState {
  items: Transaction[];
  filteredItems: Transaction[];
  filters: TransactionFilters;
  loading: boolean;
  error: string | null;
}

const initialState: TransactionsState = {
  items: [],
  filteredItems: [],
  filters: {
    startDate: null,
    endDate: null,
    categories: [],
    searchTerm: '',
  },
  loading: false,
  error: null,
};

const transactionsSlice = createSlice({
  name: 'transactions',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<TransactionFilters>) => {
      state.filters = action.payload;
      // Apply filters to items
      state.filteredItems = state.items.filter(transaction => {
        // Filter implementation
        return true; // Simplified for example
      });
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
      state.filteredItems = state.items;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTransactions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTransactions.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
        state.filteredItems = action.payload;
      })
      .addCase(fetchTransactions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setFilters, clearFilters } = transactionsSlice.actions;
export default transactionsSlice.reducer;
```

3. **Redux Hooks Usage**:

```tsx
// components/TransactionFilterForm.tsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../../store';
import { setFilters, clearFilters } from '../../store/slices/transactionsSlice';
import { DateRangePicker } from '../DateRangePicker';
import { CategorySelect } from '../CategorySelect';
import { Button } from '../Button';
import { TransactionFilters } from '../../types/Transaction.types';

export const TransactionFilterForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const currentFilters = useSelector((state: RootState) => state.transactions.filters);
  
  const [filters, setLocalFilters] = useState<TransactionFilters>(currentFilters);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(setFilters(filters));
  };
  
  const handleClear = () => {
    setLocalFilters({
      startDate: null,
      endDate: null,
      categories: [],
      searchTerm: '',
    });
    dispatch(clearFilters());
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <DateRangePicker
        startDate={filters.startDate}
        endDate={filters.endDate}
        onChange={({ startDate, endDate }) => 
          setLocalFilters(prev => ({ ...prev, startDate, endDate }))
        }
      />
      
      <CategorySelect
        selected={filters.categories}
        onChange={categories => 
          setLocalFilters(prev => ({ ...prev, categories }))
        }
      />
      
      <input
        type="text"
        placeholder="Search transactions..."
        value={filters.searchTerm}
        onChange={e => 
          setLocalFilters(prev => ({ ...prev, searchTerm: e.target.value }))
        }
      />
      
      <div className="filter-actions">
        <Button type="submit" variant="primary">Apply Filters</Button>
        <Button type="button" variant="secondary" onClick={handleClear}>Clear</Button>
      </div>
    </form>
  );
};
```

### 5.2 Local Component State

Use React's useState and useReducer for component-specific state:

```tsx
// components/Accordion.tsx
import React, { useState } from 'react';
import { styled } from 'styled-components';
import { ChevronDown, ChevronUp } from '../icons';

interface AccordionProps {
  title: string;
  children: React.ReactNode;
  initialExpanded?: boolean;
}

const AccordionWrapper = styled.div`
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 16px;
`;

const AccordionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  cursor: pointer;
  background-color: #f5f5f5;
`;

const AccordionTitle = styled.h3`
  margin: 0;
  font-size: 16px;
  font-weight: 500;
`;

const AccordionContent = styled.div<{ isExpanded: boolean }>`
  padding: ${props => props.isExpanded ? '16px' : '0'};
  max-height: ${props => props.isExpanded ? '500px' : '0'};
  overflow: hidden;
  transition: all 0.3s ease;
`;

export const Accordion: React.FC<AccordionProps> = ({ 
  title, 
  children, 
  initialExpanded = false 
}) => {
  const [isExpanded, setIsExpanded] = useState(initialExpanded);
  
  const toggleAccordion = () => {
    setIsExpanded(prev => !prev);
  };
  
  return (
    <AccordionWrapper>
      <AccordionHeader onClick={toggleAccordion}>
        <AccordionTitle>{title}</AccordionTitle>
        {isExpanded ? <ChevronUp /> : <ChevronDown />}
      </AccordionHeader>
      <AccordionContent isExpanded={isExpanded}>
        {children}
      </AccordionContent>
    </AccordionWrapper>
  );
};
```

### 5.3 Context API for Shared State

Use React Context for state that needs to be shared across components but doesn't warrant Redux:

```tsx
// contexts/ThemeContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('light');
  
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
```

## 6. API Integration

### 6.1 API Client Implementation

Use RTK Query for API integration:

```tsx
// services/api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { RootState } from '../store';
import { Transaction, TransactionFilters } from '../types/Transaction.types';
import { Budget } from '../types/Budget.types';
import { Goal } from '../types/Goal.types';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: process.env.REACT_APP_API_URL || 'https://api.pfm.example.com/api/v1',
    prepareHeaders: (headers, { getState }) => {
      // Get the token from the auth state
      const token = (getState() as RootState).auth.token;
      
      // If we have a token, add it to the request headers
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      
      return headers;
    },
  }),
  tagTypes: ['Transactions', 'Budgets', 'Goals'],
  endpoints: (builder) => ({
    // Transactions
    getTransactions: builder.query<Transaction[], TransactionFilters>({
      query: (filters) => ({
        url: '/transactions',
        params: { ...filters },
      }),
      providesTags: ['Transactions'],
    }),
    getTransactionById: builder.query<Transaction, string>({
      query: (id) => `/transactions/${id}`,
      providesTags: (result, error, id) => [{ type: 'Transactions', id }],
    }),
    createTransaction: builder.mutation<Transaction, Partial<Transaction>>({
      query: (transaction) => ({
        url: '/transactions',
        method: 'POST',
        body: transaction,
      }),
      invalidatesTags: ['Transactions'],
    }),
    updateTransaction: builder.mutation<Transaction, { id: string; transaction: Partial<Transaction> }>({
      query: ({ id, transaction }) => ({
        url: `/transactions/${id}`,
        method: 'PUT',
        body: transaction,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Transactions', id }],
    }),
    deleteTransaction: builder.mutation<void, string>({
      query: (id) => ({
        url: `/transactions/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Transactions'],
    }),
    
    // Budgets
    getBudgets: builder.query<Budget[], void>({
      query: () => '/budgets',
      providesTags: ['Budgets'],
    }),
    
    // Goals
    getGoals: builder.query<Goal[], void>({
      query: () => '/goals',
      providesTags: ['Goals'],
    }),
    
    // Additional endpoints...
  }),
});

export const {
  useGetTransactionsQuery,
  useGetTransactionByIdQuery,
  useCreateTransactionMutation,
  useUpdateTransactionMutation,
  useDeleteTransactionMutation,
  useGetBudgetsQuery,
  useGetGoalsQuery,
  // Export additional hooks...
} = api;
```

### 6.2 API Hook Usage

```tsx
// components/TransactionList.tsx
import React from 'react';
import { useGetTransactionsQuery } from '../../services/api';
import { TransactionItem } from './TransactionItem';
import { LoadingSpinner } from '../LoadingSpinner';
import { ErrorMessage } from '../ErrorMessage';
import { EmptyState } from '../EmptyState';

interface TransactionListProps {
  filters?: {
    startDate?: string;
    endDate?: string;
    categories?: string[];
  };
}

export const TransactionList: React.FC<TransactionListProps> = ({ filters = {} }) => {
  const { data: transactions, isLoading, error } = useGetTransactionsQuery(filters);
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message="Failed to load transactions" />;
  if (!transactions?.length) return <EmptyState message="No transactions found" />;
  
  return (
    <div className="transaction-list">
      {transactions.map(transaction => (
        <TransactionItem 
          key={transaction.id} 
          transaction={transaction} 
        />
      ))}
    </div>
  );
};
```

### 6.3 Error Handling

Create a centralized error handling system:

```tsx
// hooks/useErrorHandler.ts
import { useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { addNotification } from '../store/slices/notificationsSlice';
import { logoutUser } from '../store/slices/authSlice';

export const useErrorHandler = () => {
  const dispatch = useDispatch();
  
  const handleError = useCallback((error: any) => {
    // Handle network errors
    if (!error.response) {
      dispatch(addNotification({
        type: 'error',
        message: 'Network error. Please check your connection.',
      }));
      return;
    }
    
    // Handle HTTP errors
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        dispatch(addNotification({
          type: 'error',
          message: data.message || 'Invalid request',
        }));
        break;
      case 401:
        dispatch(addNotification({
          type: 'error',
          message: 'Your session has expired. Please log in again.',
        }));
        dispatch(logoutUser());
        break;
      case 403:
        dispatch(addNotification({
          type: 'error',
          message: 'You do not have permission to perform this action.',
        }));
        break;
      case 404:
        dispatch(addNotification({
          type: 'error',
          message: 'The requested resource was not found.',
        }));
        break;
      case 500:
        dispatch(addNotification({
          type: 'error',
          message: 'An unexpected error occurred. Please try again later.',
        }));
        break;
      default:
        dispatch(addNotification({
          type: 'error',
          message: data.message || 'An unexpected error occurred',
        }));
    }
  }, [dispatch]);
  
  return { handleError };
};
```

## 7. Routing and Navigation

### 7.1 Web Application Routing

Use React Router for web routing:

```tsx
// routes/index.tsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { PrivateRoute } from './PrivateRoute';
import { DashboardPage } from '../pages/DashboardPage';
import { TransactionsPage } from '../pages/TransactionsPage';
import { TransactionDetailPage } from '../pages/TransactionDetailPage';
import { BudgetsPage } from '../pages/BudgetsPage';
import { GoalsPage } from '../pages/GoalsPage';
import { InsightsPage } from '../pages/InsightsPage';
import { SettingsPage } from '../pages/SettingsPage';
import { LoginPage } from '../pages/LoginPage';
import { SignupPage } from '../pages/SignupPage';
import { NotFoundPage } from '../pages/NotFoundPage';
import { MainLayout } from '../components/layout/MainLayout';
import { AuthLayout } from '../components/layout/AuthLayout';

export const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage />
          } />
          <Route path="/signup" element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <SignupPage />
          } />
        </Route>
        
        {/* Protected Routes */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route 
            path="/dashboard" 
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/transactions" 
            element={
              <PrivateRoute>
                <TransactionsPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/transactions/:id" 
            element={
              <PrivateRoute>
                <TransactionDetailPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/budgets" 
            element={
              <PrivateRoute>
                <BudgetsPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/goals" 
            element={
              <PrivateRoute>
                <GoalsPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/insights" 
            element={
              <PrivateRoute>
                <InsightsPage />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/settings" 
            element={
              <PrivateRoute>
                <SettingsPage />
              </PrivateRoute>
            } 
          />
        </Route>
        
        {/* 404 Route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
};
```

### 7.2 Mobile Navigation

Use React Navigation for mobile navigation:

```tsx
// navigation/index.tsx
import React from 'react';
import { useSelector } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialIcons } from '@expo/vector-icons';
import { RootState } from '../store';
import { DashboardScreen } from '../screens/DashboardScreen';
import { TransactionsScreen } from '../screens/TransactionsScreen';
import { TransactionDetailScreen } from '../screens/TransactionDetailScreen';
import { BudgetsScreen } from '../screens/BudgetsScreen';
import { GoalsScreen } from '../screens/GoalsScreen';
import { InsightsScreen } from '../screens/InsightsScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { LoginScreen } from '../screens/LoginScreen';
import { SignupScreen } from '../screens/SignupScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const MainTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#1E88E5',
        tabBarInactiveTintColor: '#757575',
        tabBarLabelStyle: {
          fontSize: 12,
        },
      }}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen} 
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="dashboard" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen 
        name="Transactions" 
        component={TransactionsScreen} 
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="receipt" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen 
        name="Budgets" 
        component={BudgetsScreen} 
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="account-balance-wallet" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen 
        name="Goals" 
        component={GoalsScreen} 
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="flag" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen 
        name="Insights" 
        component={InsightsScreen} 
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialIcons name="insights" color={color} size={size} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

export const AppNavigation = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {isAuthenticated ? (
          <>
            <Stack.Screen 
              name="Main" 
              component={MainTabs} 
              options={{ headerShown: false }}
            />
            <Stack.Screen 
              name="TransactionDetail" 
              component={TransactionDetailScreen} 
              options={{ title: 'Transaction Details' }}
            />
            <Stack.Screen 
              name="Settings" 
              component={SettingsScreen} 
            />
          </>
        ) : (
          <>
            <Stack.Screen 
              name="Login" 
              component={LoginScreen} 
              options={{ headerShown: false }}
            />
            <Stack.Screen 
              name="Signup" 
              component={SignupScreen} 
              options={{ headerShown: false }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
```

## 8. Form Handling

### 8.1 Form Implementation with React Hook Form

```tsx
// components/forms/BudgetForm.tsx
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { TextField } from '../TextField';
import { Select } from '../Select';
import { DatePicker } from '../DatePicker';
import { Button } from '../Button';
import { Budget, BudgetCategory } from '../../types/Budget.types';

interface BudgetFormProps {
  initialData?: Partial<Budget>;
  categories: BudgetCategory[];
  onSubmit: (data: Budget) => void;
  isSubmitting?: boolean;
}

const schema = yup.object({
  name: yup.string().required('Budget name is required'),
  amount: yup
    .number()
    .required('Amount is required')
    .positive('Amount must be positive'),
  categoryId: yup.string().required('Category is required'),
  startDate: yup.date().required('Start date is required'),
  endDate: yup.date().required('End date is required')
    .min(
      yup.ref('startDate'), 
      'End date must be after start date'
    ),
}).required();

export const BudgetForm: React.FC<BudgetFormProps> = ({
  initialData = {},
  categories,
  onSubmit,
  isSubmitting = false,
}) => {
  const { 
    control, 
    handleSubmit, 
    formState: { errors },
    reset,
  } = useForm<Budget>({
    resolver: yupResolver(schema),
    defaultValues: {
      name: '',
      amount: 0,
      categoryId: '',
      startDate: new Date(),
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days from now
      ...initialData,
    },
  });
  
  const handleFormSubmit = (data: Budget) => {
    onSubmit(data);
    reset();
  };
  
  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <Controller
        name="name"
        control={control}
        render={({ field }) => (
          <TextField
            label="Budget Name"
            placeholder="e.g., Monthly Groceries"
            error={errors.name?.message}
            {...field}
          />
        )}
      />
      
      <Controller
        name="amount"
        control={control}
        render={({ field }) => (
          <TextField
            label="Budget Amount"
            type="number"
            placeholder="0.00"
            error={errors.amount?.message}
            {...field}
            onChange={e => field.onChange(parseFloat(e.target.value))}
          />
        )}
      />
      
      <Controller
        name="categoryId"
        control={control}
        render={({ field }) => (
          <Select
            label="Category"
            options={categories.map(cat => ({
              value: cat.id,
              label: cat.name,
            }))}
            error={errors.categoryId?.message}
            {...field}
          />
        )}
      />
      
      <div className="date-range">
        <Controller
          name="startDate"
          control={control}
          render={({ field }) => (
            <DatePicker
              label="Start Date"
              error={errors.startDate?.message}
              {...field}
            />
          )}
        />
        
        <Controller
          name="endDate"
          control={control}
          render={({ field }) => (
            <DatePicker
              label="End Date"
              error={errors.endDate?.message}
              {...field}
            />
          )}
        />
      </div>
      
      <div className="form-actions">
        <Button 
          type="submit" 
          variant="primary" 
          isLoading={isSubmitting}
          disabled={isSubmitting}
        >
          {initialData.id ? 'Update Budget' : 'Create Budget'}
        </Button>
      </div>
    </form>
  );
};
```

### 8.2 Form Validation

Use Yup for schema validation:

```tsx
// validation/transactionSchema.ts
import * as yup from 'yup';

export const transactionSchema = yup.object({
  amount: yup
    .number()
    .required('Amount is required')
    .not([0], 'Amount cannot be zero'),
  description: yup
    .string()
    .required('Description is required')
    .max(100, 'Description must be at most 100 characters'),
  date: yup
    .date()
    .required('Date is required')
    .max(new Date(), 'Date cannot be in the future'),
  categoryId: yup
    .string()
    .required('Category is required'),
  accountId: yup
    .string()
    .required('Account is required'),
  type: yup
    .string()
    .oneOf(['income', 'expense'], 'Type must be either income or expense')
    .required('Type is required'),
});
```

## 9. Testing Standards

### 9.1 Unit Testing Components

Use Jest and React Testing Library for unit tests:

```tsx
// components/Button.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button component', () => {
  it('renders correctly with default props', () => {
    render(<Button>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('button--primary'); // Default variant
    expect(button).not.toBeDisabled();
  });
  
  it('renders with the correct variant class', () => {
    render(<Button variant="secondary">Secondary Button</Button>);
    
    const button = screen.getByRole('button', { name: /secondary button/i });
    expect(button).toHaveClass('button--secondary');
  });
  
  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled Button</Button>);
    
    const button = screen.getByRole('button', { name: /disabled button/i });
    expect(button).toBeDisabled();
  });
  
  it('renders loading state when isLoading is true', () => {
    render(<Button isLoading>Loading Button</Button>);
    
    const button = screen.getByRole('button', { name: /loading button/i });
    const spinner = screen.getByTestId('button-spinner');
    
    expect(button).toBeDisabled();
    expect(spinner).toBeInTheDocument();
  });
});
```

### 9.2 Testing Hooks

```tsx
// hooks/useAuth.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { Provider } from 'react-redux';
import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import { useAuth } from './useAuth';

const mockStore = configureMockStore([thunk]);

describe('useAuth hook', () => {
  it('returns authentication state and functions', () => {
    const initialState = {
      auth: {
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      },
    };
    
    const store = mockStore(initialState);
    
    const wrapper = ({ children }) => (
      <Provider store={store}>{children}</Provider>
    );
    
    const { result } = renderHook(() => useAuth(), { wrapper });
    
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(typeof result.current.login).toBe('function');
    expect(typeof result.current.logout).toBe('function');
    expect(typeof result.current.signup).toBe('function');
  });
  
  it('dispatches login action when login is called', async () => {
    const initialState = {
      auth: {
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      },
    };
    
    const store = mockStore(initialState);
    store.dispatch = jest.fn();
    
    const wrapper = ({ children }) => (
      <Provider store={store}>{children}</Provider>
    );
    
    const { result } = renderHook(() => useAuth(), { wrapper });
    
    const credentials = {
      email: 'test@example.com',
      password: 'password123',
    };
    
    await act(async () => {
      await result.current.login(credentials);
    });
    
    expect(store.dispatch).toHaveBeenCalledTimes(1);
    // Verify the action type here based on your implementation
  });
});
```

### 9.3 Integration Testing

```tsx
// features/auth/Login.integration.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import configureStore from '../../store/configureStore';
import { LoginPage } from '../../pages/LoginPage';

describe('Login Integration Tests', () => {
  it('logs in user successfully', async () => {
    // Mock API response
    global.fetch = jest.fn().mockImplementation(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          user: { id: '123', email: 'test@example.com', name: 'Test User' },
          token: 'fake-token',
        }),
      })
    );
    
    const store = configureStore();
    
    render(
      <Provider store={store}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </Provider>
    );
    
    // Fill in the login form
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));
    
    // Wait for the login process to complete
    await waitFor(() => {
      const state = store.getState().auth;
      expect(state.isAuthenticated).toBe(true);
      expect(state.user.email).toBe('test@example.com');
      expect(state.token).toBe('fake-token');
    });
    
    // Clean up
    global.fetch.mockClear();
    delete global.fetch;
  });
  
  it('shows error message for invalid credentials', async () => {
    // Mock API error response
    global.fetch = jest.fn().mockImplementation(() => 
      Promise.resolve({
        ok: false,
        status: 401,
        json: () => Promise.resolve({
          message: 'Invalid email or password',
        }),
      })
    );
    
    const store = configureStore();
    
    render(
      <Provider store={store}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </Provider>
    );
    
    // Fill in the login form with invalid credentials
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpassword' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /log in/i }));
    
    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText(/invalid email or password/i)).toBeInTheDocument();
    });
    
    // The user should not be authenticated
    expect(store.getState().auth.isAuthenticated).toBe(false);
    
    // Clean up
    global.fetch.mockClear();
    delete global.fetch;
  });
});
```

## 10. Custom Hooks

### 10.1 Feature-Specific Hooks

Create custom hooks for feature-specific logic:

```tsx
// hooks/useTransactions.ts
import { useCallback, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchTransactions, 
  addTransaction, 
  updateTransaction, 
  deleteTransaction, 
  setFilters, 
  clearFilters 
} from '../store/slices/transactionsSlice';
import { RootState, AppDispatch } from '../store';
import { Transaction, TransactionFilters } from '../types/Transaction.types';
import { useErrorHandler } from './useErrorHandler';

export const useTransactions = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { handleError } = useErrorHandler();
  
  const { 
    items, 
    filteredItems, 
    filters, 
    loading, 
    error 
  } = useSelector((state: RootState) => state.transactions);
  
  const fetchTransactionsData = useCallback(async () => {
    try {
      await dispatch(fetchTransactions(filters)).unwrap();
    } catch (error) {
      handleError(error);
    }
  }, [dispatch, filters, handleError]);
  
  const createTransaction = useCallback(async (transaction: Partial<Transaction>) => {
    try {
      await dispatch(addTransaction(transaction)).unwrap();
    } catch (error) {
      handleError(error);
      throw error;
    }
  }, [dispatch, handleError]);
  
  const modifyTransaction = useCallback(async (id: string, transaction: Partial<Transaction>) => {
    try {
      await dispatch(updateTransaction({ id, transaction })).unwrap();
    } catch (error) {
      handleError(error);
      throw error;
    }
  }, [dispatch, handleError]);
  
  const removeTransaction = useCallback(async (id: string) => {
    try {
      await dispatch(deleteTransaction(id)).unwrap();
    } catch (error) {
      handleError(error);
      throw error;
    }
  }, [dispatch, handleError]);
  
  const updateFilters = useCallback((newFilters: TransactionFilters) => {
    dispatch(setFilters(newFilters));
  }, [dispatch]);
  
  const resetFilters = useCallback(() => {
    dispatch(clearFilters());
  }, [dispatch]);
  
  const totalIncome = useMemo(() => {
    return filteredItems
      .filter(t => t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0);
  }, [filteredItems]);
  
  const totalExpenses = useMemo(() => {
    return filteredItems
      .filter(t => t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);
  }, [filteredItems]);
  
  const balance = useMemo(() => {
    return totalIncome - totalExpenses;
  }, [totalIncome, totalExpenses]);
  
  return {
    transactions: filteredItems,
    filters,
    loading,
    error,
    totalIncome,
    totalExpenses,
    balance,
    fetchTransactions: fetchTransactionsData,
    createTransaction,
    updateTransaction: modifyTransaction,
    deleteTransaction: removeTransaction,
    updateFilters,
    resetFilters,
  };
};
```

### 10.2 Utility Hooks

Create reusable utility hooks:

```tsx
// hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);
  
  return debouncedValue;
};
```

```tsx
// hooks/useLocalStorage.ts
import { useState, useEffect } from 'react';

export const useLocalStorage = <T>(
  key: string, 
  initialValue: T
): [T, (value: T) => void] => {
  // Get initial value from localStorage or use initialValue
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });
  
  // Update localStorage when storedValue changes
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);
  
  return [storedValue, setStoredValue];
};
```

## 11. Implementing a New Feature

Here's a step-by-step guide for implementing a new feature in the frontend applications:

### 11.1 Example: Adding a Transaction Categorization Feature

1. **Define Types**:

```tsx
// types/Transaction.types.ts
export interface TransactionCategory {
  id: string;
  name: string;
  color: string;
  icon?: string;
}

// Add to Transaction interface
export interface Transaction {
  id: string;
  amount: number;
  description: string;
  date: Date;
  type: 'income' | 'expense';
  accountId: string;
  categoryId?: string; // Optional, may be uncategorized
  category?: TransactionCategory; // Optional, populated from relation
  // ... other fields
}

export interface TransactionCategorizationRequest {
  categoryId: string;
}
```

2. **Add API Endpoint**:

```tsx
// services/api.ts
// Add to existing API definition
categorizeTransaction: builder.mutation<
  Transaction, 
  { id: string; categoryId: string }
>({
  query: ({ id, categoryId }) => ({
    url: `/transactions/${id}/categorize`,
    method: 'PUT',
    body: { categoryId },
  }),
  invalidatesTags: (result, error, { id }) => [
    { type: 'Transactions', id }
  ],
}),

// Export the hook
export const { 
  // ... existing exports
  useCategorizeTransactionMutation,
} = api;
```

3. **Create UI Components**:

```tsx
// components/CategorySelector.tsx
import React from 'react';
import { styled } from 'styled-components';
import { TransactionCategory } from '../types/Transaction.types';

interface CategorySelectorProps {
  categories: TransactionCategory[];
  selectedCategoryId?: string;
  onSelectCategory: (categoryId: string) => void;
}

const CategoryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
`;

const CategoryItem = styled.div<{ isSelected: boolean; color: string }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  border: 2px solid ${props => props.isSelected ? props.color : 'transparent'};
  background-color: ${props => props.isSelected ? `${props.color}20` : '#f5f5f5'};
  
  &:hover {
    background-color: ${props => `${props.color}10`};
  }
`;

const CategoryIcon = styled.div<{ color: string }>`
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background-color: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  color: white;
`;

const CategoryName = styled.span`
  font-size: 12px;
  text-align: center;
`;

export const CategorySelector: React.FC<CategorySelectorProps> = ({
  categories,
  selectedCategoryId,
  onSelectCategory,
}) => {
  return (
    <CategoryGrid>
      {categories.map(category => (
        <CategoryItem
          key={category.id}
          isSelected={category.id === selectedCategoryId}
          color={category.color}
          onClick={() => onSelectCategory(category.id)}
        >
          <CategoryIcon color={category.color}>
            {category.icon || category.name.charAt(0)}
          </CategoryIcon>
          <CategoryName>{category.name}</CategoryName>
        </CategoryItem>
      ))}
    </CategoryGrid>
  );
};
```

4. **Create Feature Component**:

```tsx
// features/transactions/TransactionCategorization.tsx
import React, { useState } from 'react';
import { styled } from 'styled-components';
import { useCategorizeTransactionMutation } from '../../services/api';
import { useGetCategoriesQuery } from '../../services/api';
import { CategorySelector } from '../../components/CategorySelector';
import { Button } from '../../components/Button';
import { Transaction } from '../../types/Transaction.types';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { ErrorMessage } from '../../components/ErrorMessage';

interface TransactionCategorizationProps {
  transaction: Transaction;
  onSuccess?: () => void;
  onCancel?: () => void;
}

const Container = styled.div`
  padding: 16px;
`;

const Title = styled.h3`
  margin-top: 0;
  margin-bottom: 16px;
`;

const Actions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
`;

export const TransactionCategorization: React.FC<TransactionCategorizationProps> = ({
  transaction,
  onSuccess,
  onCancel,
}) => {
  const [selectedCategoryId, setSelectedCategoryId] = useState<string>(
    transaction.categoryId || ''
  );
  
  const { data: categories, isLoading: categoriesLoading, error: categoriesError } = 
    useGetCategoriesQuery();
    
  const [categorizeTransaction, { isLoading: isSubmitting }] = 
    useCategorizeTransactionMutation();
  
  const handleSubmit = async () => {
    if (!selectedCategoryId) return;
    
    try {
      await categorizeTransaction({
        id: transaction.id,
        categoryId: selectedCategoryId,
      }).unwrap();
      
      if (onSuccess) onSuccess();
    } catch (error) {
      console.error('Failed to categorize transaction:', error);
    }
  };
  
  if (categoriesLoading) return <LoadingSpinner />;
  if (categoriesError) return <ErrorMessage message="Failed to load categories" />;
  if (!categories) return <ErrorMessage message="No categories available" />;
  
  return (
    <Container>
      <Title>Categorize Transaction</Title>
      <p>Select a category for this transaction:</p>
      
      <CategorySelector
        categories={categories}
        selectedCategoryId={selectedCategoryId}
        onSelectCategory={setSelectedCategoryId}
      />
      
      <Actions>
        <Button 
          variant="secondary" 
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button 
          variant="primary" 
          onClick={handleSubmit}
          disabled={!selectedCategoryId || isSubmitting}
          isLoading={isSubmitting}
        >
          Save
        </Button>
      </Actions>
    </Container>
  );
};
```

5. **Add the Feature to the Transaction Detail Page**:

```tsx
// pages/TransactionDetailPage.tsx
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGetTransactionByIdQuery } from '../services/api';
import { TransactionCategorization } from '../features/transactions/TransactionCategorization';
import { TransactionDetail } from '../features/transactions/TransactionDetail';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';
import { PageLayout } from '../components/layout/PageLayout';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';

export const TransactionDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [isCategorizeModalOpen, setIsCategorizeModalOpen] = useState(false);
  
  const { 
    data: transaction,
    isLoading,
    error,
    refetch
  } = useGetTransactionByIdQuery(id as string);
  
  const handleBack = () => {
    navigate('/transactions');
  };
  
  const handleCategorizationSuccess = () => {
    setIsCategorizeModalOpen(false);
    refetch();
  };
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message="Failed to load transaction" />;
  if (!transaction) return <ErrorMessage message="Transaction not found" />;
  
  return (
    <PageLayout title="Transaction Details" onBack={handleBack}>
      <TransactionDetail transaction={transaction} />
      
      <Button
        variant="secondary"
        onClick={() => setIsCategorizeModalOpen(true)}
      >
        {transaction.categoryId ? 'Recategorize' : 'Categorize'} Transaction
      </Button>
      
      <Modal
        isOpen={isCategorizeModalOpen}
        onClose={() => setIsCategorizeModalOpen(false)}
        title="Categorize Transaction"
      >
        <TransactionCategorization
          transaction={transaction}
          onSuccess={handleCategorizationSuccess}
          onCancel={() => setIsCategorizeModalOpen(false)}
        />
      </Modal>
    </PageLayout>
  );
};
```

## 12. Cross-Cutting Concerns

### 12.1 Localization

Use react-intl for internationalization:

```tsx
// App.tsx
import React from 'react';
import { IntlProvider } from 'react-intl';
import { useSelector } from 'react-redux';
import { RootState } from './store';
import { AppRoutes } from './routes';
import enMessages from './locales/en.json';
import esMessages from './locales/es.json';
import frMessages from './locales/fr.json';

const messages = {
  en: enMessages,
  es: esMessages,
  fr: frMessages,
};

export const App: React.FC = () => {
  const { locale } = useSelector((state: RootState) => state.settings);
  
  return (
    <IntlProvider
      locale={locale}
      messages={messages[locale]}
      defaultLocale="en"
    >
      <AppRoutes />
    </IntlProvider>
  );
};
```

Using translations in components:

```tsx
// components/TransactionSummary.tsx
import React from 'react';
import { FormattedMessage, FormattedNumber, useIntl } from 'react-intl';
import { styled } from 'styled-components';

interface TransactionSummaryProps {
  income: number;
  expenses: number;
  currency?: string;
}

const SummaryContainer = styled.div`
  padding: 16px;
  border-radius: 8px;
  background-color: #f5f5f5;
  margin-bottom: 24px;
`;

const SummaryRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
`;

const BalanceRow = styled(SummaryRow)`
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
  font-weight: bold;
`;

export const TransactionSummary: React.FC<TransactionSummaryProps> = ({
  income,
  expenses,
  currency = 'USD',
}) => {
  const intl = useIntl();
  const balance = income - expenses;
  
  return (
    <SummaryContainer>
      <SummaryRow>
        <span>
          <FormattedMessage id="transactions.summary.income" defaultMessage="Income" />
        </span>
        <span>
          <FormattedNumber
            value={income}
            style="currency"
            currency={currency}
          />
        </span>
      </SummaryRow>
      
      <SummaryRow>
        <span>
          <FormattedMessage id="transactions.summary.expenses" defaultMessage="Expenses" />
        </span>
        <span>
          <FormattedNumber
            value={expenses}
            style="currency"
            currency={currency}
          />
        </span>
      </SummaryRow>
      
      <BalanceRow>
        <span>
          <FormattedMessage id="transactions.summary.balance" defaultMessage="Balance" />
        </span>
        <span style={{ color: balance >= 0 ? '#4CAF50' : '#F44336' }}>
          <FormattedNumber
            value={balance}
            style="currency"
            currency={currency}
          />
        </span>
      </BalanceRow>
    </SummaryContainer>
  );
};
```

### 12.2 Accessibility

Implement accessibility features:

```tsx
// components/TextField.tsx
import React, { forw