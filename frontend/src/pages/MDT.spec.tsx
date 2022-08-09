import React from 'react';

// LIBRARIES
import '@testing-library/jest-dom';
import { render, screen, act, waitFor } from '@testing-library/react';
import { composeStories } from '@storybook/testing-react';
import userEvent from '@testing-library/user-event';

// LOCAL IMPORTS
import * as stories from './MDT.stories';

const { Default, Locked } = composeStories(stories);

describe('When the page loads', () => {
  it('Should display the loading spinner and then disappear', async () => {
    jest.useFakeTimers();
    render(
      <Default />,
    );
    expect(screen.getByText(/loading.svg/i)).toBeInTheDocument();

    await act(async () => {
      jest.setSystemTime(Date.now() + 10000);
      jest.advanceTimersByTime(1000);
    });
    expect(screen.queryByText(/loading.svg/i)).not.toBeInTheDocument();
  });

  it('Should show patient demographics and reason for mdt referral', async () => {
    jest.useFakeTimers();
    render(
      <Default />,
    );
    expect(screen.getByText(/loading.svg/i)).toBeInTheDocument();

    await act(async () => {
      jest.setSystemTime(Date.now() + 10000);
      jest.advanceTimersByTime(1000);
    });
    expect(screen.queryByText(/loading.svg/i)).not.toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('First Last (1)')).toBeInTheDocument();
      expect(screen.getByText('fMRN: 0000001L')).toBeInTheDocument();
      expect(screen.getByText('fNHS: 000-000-1L')).toBeInTheDocument();
      expect(screen.getByText(new Date('01/01/2000').toLocaleDateString())).toBeInTheDocument();
      expect(screen.getByText('reason goes here (1)')).toBeInTheDocument();
    });
  });
});

const renderEdit = (async () => {
  const { click } = userEvent.setup();
  jest.useFakeTimers();
  render(
    <Default />,
  );
  expect(screen.getByText(/loading.svg/i)).toBeInTheDocument();

  await act(async () => {
    jest.setSystemTime(Date.now() + 10000);
    jest.advanceTimersByTime(1000);
  });
  expect(screen.queryByText(/loading.svg/i)).not.toBeInTheDocument();

  click(screen.getAllByText(/edit/i)[0]);
  await waitFor(() => {
    expect(screen.getByText(/mdt management/i)).toBeInTheDocument();
  });
});

describe('Clicking edit on a patient row', () => {
  it('Should show the edit modal', async () => {
    const { click } = userEvent.setup();
    jest.useFakeTimers();
    render(
      <Default />,
    );
    expect(screen.getByText(/loading.svg/i)).toBeInTheDocument();

    await act(async () => {
      jest.setSystemTime(Date.now() + 10000);
      jest.advanceTimersByTime(1000);
    });
    expect(screen.queryByText(/loading.svg/i)).not.toBeInTheDocument();

    click(screen.getAllByText(/edit/i)[0]);
    await waitFor(() => {
      expect(screen.getByText(/mdt management/i)).toBeInTheDocument();
    });
  });
  it('it should autocomplete with data from query', async () => {
    await renderEdit();
    expect((screen.getByLabelText(/reason added to mdt/i) as HTMLInputElement)).toHaveValue('reason goes here (1)');
  });
  it('Should show an error if already locked', async () => {
    const { click } = userEvent.setup();
    jest.useFakeTimers();
    render(
      <Locked />,
    );
    expect(screen.getByText(/loading.svg/i)).toBeInTheDocument();

    await act(async () => {
      jest.setSystemTime(Date.now() + 10000);
      jest.advanceTimersByTime(1000);
    });
    expect(screen.queryByText(/loading.svg/i)).not.toBeInTheDocument();

    click(screen.getAllByText(/edit/i)[0]);
    await waitFor(() => {
      expect(screen.getByText(/locked by someone else/i)).toBeInTheDocument();
    });
  });
});
