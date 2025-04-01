// src/components/StyledCard.tsx
import styled from 'styled-components';

export const Card = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin: 1rem 0;
`;

export const Title = styled.h2`
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 1rem;
`;

export const Price = styled.p`
  color: #666;
  font-size: 1.2rem;
  span {
    color: #ff5a5f;
    font-weight: bold;
  }
`;