# Restaurant Management System - Data Flow Diagrams

## Context Diagram (Level 0)

```mermaid
graph TD
    U[User] --> |Login/Signup Details| S[Restaurant Management System]
    A[Admin] --> |Restaurant/Menu Management| S
    S --> |Restaurant/Menu Information| U
    S --> |Dashboard/Management Data| A
    S --> |Authentication Response| U
    S --> |Authentication Response| A
```

## Level 1 DFD

```mermaid
graph TD
    %% External Entities
    U[User] 
    A[Admin]
    
    %% Processes
    P1((1.0<br/>User Authentication))
    P2((2.0<br/>Restaurant Management))
    P3((3.0<br/>Menu Management))
    P4((4.0<br/>Admin Dashboard))
    
    %% Data Stores
    DS1[(User DB)]
    DS2[(Restaurant DB)]
    DS3[(Menu Items DB)]
    
    %% Data Flows - Users
    U -->|Login/Signup Details| P1
    P1 -->|User Data| DS1
    DS1 -->|Validation| P1
    P1 -->|Auth Response| U
    
    %% Data Flows - Admin
    A -->|Admin Credentials| P1
    P1 -->|Auth Status| P4
    A -->|Restaurant Updates| P2
    A -->|Menu Updates| P3
    
    %% Restaurant Management Flows
    P2 -->|Restaurant Data| DS2
    DS2 -->|Restaurant List| P2
    P2 -->|Restaurant Info| U
    P2 -->|Restaurant Stats| P4
    
    %% Menu Management Flows
    P3 -->|Menu Items| DS3
    DS3 -->|Menu Data| P3
    P3 -->|Menu Info| U
    P3 -->|Menu Stats| P4
    
    %% Dashboard Flows
    P4 -->|Dashboard Data| A
```

## Level 2 DFD - User Authentication Process (1.0)

```mermaid
graph TD
    %% External Entities
    U[User/Admin]
    
    %% Processes
    P1.1((1.1<br/>Login))
    P1.2((1.2<br/>Signup))
    P1.3((1.3<br/>Session<br/>Management))
    P1.4((1.4<br/>Password<br/>Handling))
    
    %% Data Store
    DS1[(User DB)]
    
    %% Data Flows
    U -->|Login Credentials| P1.1
    U -->|Signup Details| P1.2
    P1.1 -->|User Data Query| DS1
    P1.2 -->|New User Data| DS1
    DS1 -->|User Info| P1.1
    P1.4 -->|Hashed Password| DS1
    P1.2 -->|Password| P1.4
    P1.1 -->|Session Data| P1.3
    P1.3 -->|Session Cookie| U
```

## Level 2 DFD - Restaurant Management Process (2.0)

```mermaid
graph TD
    %% External Entities
    A[Admin]
    U[User]
    
    %% Processes
    P2.1((2.1<br/>Add/Edit<br/>Restaurant))
    P2.2((2.2<br/>Delete<br/>Restaurant))
    P2.3((2.3<br/>View<br/>Restaurants))
    P2.4((2.4<br/>Category<br/>Management))
    
    %% Data Store
    DS2[(Restaurant DB)]
    
    %% Data Flows
    A -->|Restaurant Details| P2.1
    A -->|Delete Request| P2.2
    P2.1 -->|Restaurant Data| DS2
    P2.2 -->|Delete Query| DS2
    DS2 -->|Restaurant List| P2.3
    P2.3 -->|Restaurant Info| U
    P2.4 -->|Category Updates| DS2
    DS2 -->|Category Data| P2.4
```

## Level 2 DFD - Menu Management Process (3.0)

```mermaid
graph TD
    %% External Entities
    A[Admin]
    U[User]
    
    %% Processes
    P3.1((3.1<br/>Add/Edit<br/>Menu Items))
    P3.2((3.2<br/>Delete<br/>Menu Items))
    P3.3((3.3<br/>View<br/>Menu))
    P3.4((3.4<br/>Price<br/>Management))
    
    %% Data Stores
    DS2[(Restaurant DB)]
    DS3[(Menu Items DB)]
    
    %% Data Flows
    A -->|Menu Item Details| P3.1
    A -->|Delete Request| P3.2
    P3.1 -->|Menu Data| DS3
    P3.2 -->|Delete Query| DS3
    DS3 -->|Menu List| P3.3
    DS2 -->|Restaurant Info| P3.3
    P3.3 -->|Menu Info| U
    P3.4 -->|Price Updates| DS3
    DS3 -->|Price Data| P3.4
```

The above Data Flow Diagrams represent:

1. **Context Diagram (Level 0)**: Shows the system's interaction with external entities (Users and Admins)
2. **Level 1 DFD**: Breaks down the main system into major processes and shows data stores
3. **Level 2 DFDs**: Detailed breakdown of major processes:
   - User Authentication Process (1.0)
   - Restaurant Management Process (2.0)
   - Menu Management Process (3.0)

Key Components:
- **Processes**: Shown as circles/ovals
- **External Entities**: Shown as rectangles
- **Data Stores**: Shown as open-ended rectangles
- **Data Flows**: Shown as arrows with descriptions
