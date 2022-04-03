import '../src/bootstrap.min.css';
import 'nhsuk-frontend/dist/nhsuk.css';

// Bootstrap imports first so other modules can override
import '../src/index.css';
import { MockedProvider } from '@apollo/client/testing';
import { cache } from '../src/app/cache';
import { Provider } from 'react-redux';
import store from '../src/app/store';

export const decorators = [
  (Story) => (
    <Provider store= { store }>
      <Story />
    </Provider>
  ),
];

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  apolloClient: {
    MockedProvider,
    cache: cache
    // any props you want to pass to MockedProvider on every story
  },
}