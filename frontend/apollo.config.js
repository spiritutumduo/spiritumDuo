module.exports = {
  client: {
    service: {
      name: 'Spiritum Duo',
      url: 'http://localhost:8080/graphql',
    },
    excludes: ['**/__generated__/**', '**/schema.graphql'],
  },
};
