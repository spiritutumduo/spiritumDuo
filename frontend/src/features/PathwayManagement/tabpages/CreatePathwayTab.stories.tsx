import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import { MemoryRouter } from 'react-router';
import { MockAuthProvider, MockPathwayProvider } from 'test/mocks/mockContext';
import { cache } from 'app/cache';
import { NewMockSdApolloProvider } from 'test/mocks/mockApolloProvider';
import CreatePathwayTab, { CREATE_PATHWAY_MUTATION } from './CreatePathwayTab';

const clinicalRequestTypes = [
  {
    id: '1',
    name: 'Test clinicalRequest type 1',
    refName: 'ref test clinicalRequest type 1',
  },
  {
    id: '2',
    name: 'Test clinicalRequest type 2',
    refName: 'ref test clinicalRequest type 2',
  },
];

const successfulPathwayCreationResult = {
  pathway: {
    id: '1',
    name: 'test pathway',
    clinicalRequestTypes: [
      {
        id: '1',
        name: 'test clinicalRequest one',
        refName: 'ref test clinicalRequest one',
      },
      {
        id: '2',
        name: 'test clinicalRequest two',
        refName: 'ref test clinicalRequest two',
      },
    ],
  },
  userErrors: null,
};

const errorPathwayCreationResult = {
  pathway: null,
  userErrors: [{
    field: 'name',
    message: 'a pathway with that name already exists',
  }],
};

export default {
  title: 'Tab Pages/Pathway Management/Create Pathway Tab',
  component: CreatePathwayTab,
  decorators: [
    (CreatePathwayTabStory) => {
      cache.reset();
      return (
        <MemoryRouter>
          <MockAuthProvider>
            <MockPathwayProvider>
              <CreatePathwayTabStory />
            </MockPathwayProvider>
          </MockAuthProvider>
        </MemoryRouter>
      );
    },
  ],
} as ComponentMeta<typeof CreatePathwayTab>;

export const Default: ComponentStory<typeof CreatePathwayTab> = () => (
  <NewMockSdApolloProvider
    mocks={
      [{
        query: CREATE_PATHWAY_MUTATION,
        mockFn: () => Promise.resolve({
          data: {
            createPathway: successfulPathwayCreationResult,
          },
        }),
      }]
    }
  >
    <CreatePathwayTab
      disableForm={ false }
      clinicalRequestTypes={ clinicalRequestTypes }
    />
  </NewMockSdApolloProvider>
);

export const PathwayExistsError: ComponentStory<typeof CreatePathwayTab> = () => (
  <NewMockSdApolloProvider
    mocks={
      [{
        query: CREATE_PATHWAY_MUTATION,
        mockFn: () => Promise.resolve({
          data: {
            createPathway: errorPathwayCreationResult,
          },
        }),
      }]
    }
  >
    <CreatePathwayTab
      clinicalRequestTypes={ clinicalRequestTypes }
    />
  </NewMockSdApolloProvider>
);
