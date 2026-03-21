const express = require('express');
const app = express();
const mongoose = require('mongoose');
const routes = require('./routes/index');
const dotenv = require('dotenv');
dotenv.config();

app.use(express.json());
app.use('/api', routes);

mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:' ));
db.once('open', function () {
  console.log('Connected to MongoDB');
});

app.listen(process.env.PORT, () => {
  console.log(`Server listening on port ${process.env.PORT}`);
});