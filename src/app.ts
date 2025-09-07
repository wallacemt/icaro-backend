import cors from 'cors';
import dotenv from 'dotenv';
import express, { type Application } from 'express';
import swaggerUi from 'swagger-ui-express';
import { StatusController } from './controllers/statusController';
// import { AuthController } from './controllers/authController';

import { swaggerSpec } from './docs/swaggerConfiguration';
import { env } from './env';
import { requestLogger } from './middleware/requestLogger';
import { devDebugger } from './utils/devDebugger';

dotenv.config();
class App {
   app: Application;
  constructor() {
    this.app = express();
    this.config();
    this.routes();
    this.listen(env.PORT || 3000);
  }
  routes() {
    this.app.get('/', (_req, res) => res.redirect('/docs'));
    this.app.use('/status', new StatusController().router);
    // this.app.use('/auth', new AuthController().router);

   
    this.app.use(
      '/docs',
      swaggerUi.serve,
      swaggerUi.setup(swaggerSpec, {
        swaggerOptions: {
          validatorUrl: null,
          tryItOutEnabled: true,
          displayRequestDuration: true,
        },
      })
    );
  }
  config() {
    this.app.use(
      cors({
        origin: env.FRONTEND_URL,
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
      })
    );
    this.app.use(requestLogger);
    this.app.use(express.json());
  }
  listen(port: number | string) {
    this.app.listen(port, () =>
      devDebugger(`Servidor rodando na porta ${port}`)
    );
  }
}

export default new App().app;
