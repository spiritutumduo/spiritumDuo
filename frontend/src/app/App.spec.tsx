/* eslint-disable @typescript-eslint/no-empty-function */
/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
// we want fetchMock to prevent any accidental logins, even though we
// don't test login here
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import fetchMock from 'fetch-mock';
import { MockedProvider } from '@apollo/client/testing';
import { AuthContext, AuthContextInterface, PathwayContext, PathwayContextInterface } from 'app/context';
import User from 'types/Users';
import PathwayOption from 'types/PathwayOption';
import { MemoryRouter } from 'react-router';
import store from 'app/store';
import { Provider } from 'react-redux';
import App from './App';

const fakeUser: User = {
  id: '1',
  firstName: 'Test-John',
  lastName: 'Test-Doe',
  department: 'Respiratory',
  roles: [],
  defaultPathwayId: 1,
  token: 'token',
};

const fakePathways: PathwayOption[] = [
  {
    id: 1,
    name: 'Lung Cancer Test',
  },
  {
    id: 2,
    name: 'Bronchieactasis Test',
  },
];

const mockAuthProviderProps: AuthContextInterface = {
  updateUser: () => {},
  user: fakeUser,
};

const mockPathwayProviderProps: PathwayContextInterface = {
  pathwayOptions: fakePathways,
  currentPathwayId: fakePathways[0].id,
  updateCurrentPathwayId: () => {},
  updatePathwayOptions: () => {},
};

interface AppElementProps {
  authProviderProps?: AuthContextInterface,
  pathwayProviderProps?: PathwayContextInterface,
}

const renderApp = async (props?: AppElementProps) => {
  render(
    <Provider store={ store }>
      <MockedProvider>
        <AuthContext.Provider value={ props?.authProviderProps || mockAuthProviderProps }>
          <PathwayContext.Provider
            value={ props?.pathwayProviderProps || mockPathwayProviderProps }
          >
            <MemoryRouter>
              <App />
            </MemoryRouter>
          </PathwayContext.Provider>
        </AuthContext.Provider>
      </MockedProvider>
    </Provider>,
  );
};

test('Should render login page with no user in context', () => {
  renderApp({
    authProviderProps: {
      user: undefined,
      updateUser: () => {},
    },
  });
  expect(screen.getByRole('textbox', { name: 'Username' })).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});

test('Should render home page with valid user and pathways', () => {
  renderApp();
  expect(screen.getByText(/To do/i)).toBeInTheDocument();
});

test('Should display error if no pathways present while logged in', () => {
  renderApp({
    pathwayProviderProps: {
      pathwayOptions: [],
      updateCurrentPathwayId: () => {},
      updatePathwayOptions: () => {},
    },
  });
  expect(screen.getByText(/application not configured/i)).toBeInTheDocument();
});
