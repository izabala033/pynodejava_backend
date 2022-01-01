/** source/controllers/posts.ts */
import { Request, Response, NextFunction } from 'express';


//currently not used
interface Location {
    name: String;
    cp: String;
    city: String;
}


// getting all posts
const getLocs = async (req: Request, res: Response, next: NextFunction) => {
    let cp: any = req.query.cp;

    var sqlite3 = require("sqlite3").verbose();
    var db = new sqlite3.Database("db.sqlite3", (err: Error) => {
        if (err) {
          console.error(err.message);
          return res.status(401).json({"error": "an error happened opening the database"});
        }
      });

    const rows = db.all(
        'SELECT name, cp, city FROM location_location INNER JOIN location_sherpauser on location_location.name_id = location_sherpauser.id    WHERE cp = ?',
        [cp],
        (err: Error, row: any) => { //async response
          if (err) {
            console.log(err)
            return res.status(401).json({"error": "an error happened"});
            //throw err
          }
          db.close((err: Error) => {
            if (err) {
              console.error(err.message);
              return res.status(401).json({"error": "an error happened closing the database"});
            }
          });
          return res.status(200).json({row});
        });

        
};


const deleteLoc = async (req: Request, res: Response, next: NextFunction) => {
   
    let cp: any = req.query.cp;

    var sqlite3 = require("sqlite3").verbose();
    var db = new sqlite3.Database("db.sqlite3", (err: Error) => {
        if (err) {
          console.error(err.message);
          return res.status(401).json({"error": "an error happened opening the database"});
        }
      });

    const rows = db.run(
        'DELETE FROM location_location WHERE cp = ?',
        [cp],
        (err: Error, row: any) => { //async response
          if (err) {
            console.log(err)
            return res.status(401).json({"error": "an error happened"});
            //throw err
          }
          db.close((err: Error) => {
            if (err) {
              console.error(err.message);
              return res.status(401).json({"error": "an error happened closing the database"});
            }
          });
          return res.status(200).json({"message":"data has been deleted succesfully"});
        });

};



export default { getLocs, deleteLoc };