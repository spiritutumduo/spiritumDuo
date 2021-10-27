/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import { Story, Meta } from '@storybook/react';
import { DefaultLayout } from 'components/PageLayout.stories';
import StoryRouter from 'storybook-react-router';
import { PageLayoutProps } from 'components/PageLayout';
import PatientPage, { PatientPageProps } from './Patient';

export default {
  title: 'Pages/Patient',
  component: PatientPage,
  decorators: [StoryRouter()],
} as Meta<typeof PatientPage>;

const Template: Story<PatientPageProps> = (args: PatientPageProps) => <PatientPage { ...args } />;

export const Default = Template.bind({});
Default.args = {
  pageLayoutProps: { ...DefaultLayout.args as PageLayoutProps },
  patient: {
    id: 2,
    patientHospitalNumber: 'MRN0123456',
    firstName: 'John',
    lastName: 'Doe',
    dob: new Date('1942-11-25'),
  },
  decisions: [
    {
      date: new Date('2021-10-17'),
      decision: 'Clinic',
    },
    {
      date: new Date('2021-10-01'),
      decision: 'MDT',
    },
    {
      date: new Date('2021-11-09'),
      decision: 'Follow Up',
    },
  ],
  notes: [
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer',
      note: 'Called back, patient says unwell, stayed at home',
    },
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer',
      note: 'Called back, patient says unwell, stayed at home',
    },
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer',
      note: 'Called back, patient says unwell, stayed at home',
    },
  ],
  messages: [
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer to Tony Tottle',
      note: 'Tony, have you looked at that nodule yet?',
    },
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer to Tony Tottle',
      note: 'Tony, have you looked at that nodule yet?',
    },
    {
      date: new Date('2021-07-11'),
      enteredBy: 'Henry Steer to Tony Tottle',
      note: 'Tony, have you looked at that nodule yet?',
    },
  ],
};