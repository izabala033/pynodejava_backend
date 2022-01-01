/** source/routes/posts.ts */
import express from 'express';
import controller from '../controllers/posts';
const router = express.Router();

router.get('/getLocs', controller.getLocs);
router.delete('/deleteLocs', controller.deleteLoc);
router.get('/deleteLocs', controller.deleteLoc);

export = router;