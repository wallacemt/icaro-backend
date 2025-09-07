import swaggerJSDoc from 'swagger-jsdoc';

export const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Icaro Backend API',
      version: '1.0.0',
      description:
        'Documentação da projeto icaro, com as rotas e modelos de dados da API.',
    },
    servers: [
      {
        url: 'http://localhost:8081',
        description: 'Servidor de Desenvolvimento',
      },
      {
        url: 'https://icaro-backend.onrender.com',
        description: 'Servidor de Produção',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
    },
    security: [{ bearerAuth: [] }],
  },
  apis: [
    './src/controllers/**/*.ts',
    './src/docs/schemas/*.yaml',
    './src/docs/paths/*.yaml',
  ],
};

export const swaggerSpec = swaggerJSDoc(swaggerOptions);
