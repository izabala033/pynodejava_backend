
package com.sherpa.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.sql.*;
import java.util.HashMap;
import com.google.gson.Gson;

@RestController
public class UrlController {
  // private final String

  final String dbpath = "jdbc:sqlite:/D:/db.sqlite3";


  @GetMapping("/count")
  public String getCount() {

    Connection c = null;
    Statement stmt = null;
    ResultSet rs = null;
    HashMap<String, Integer> cp_count = new HashMap<String, Integer>();
    Gson gson = new Gson();

    try {
      Class.forName("org.sqlite.JDBC");
      c = DriverManager.getConnection(dbpath);

      System.out.println("Opened database successfully");
      stmt = c.createStatement();

      System.out.println("accessing db");
      rs = stmt.executeQuery("SELECT cp, count(*) FROM location_location group by(cp);");

      while (rs.next()) {
        cp_count.put(rs.getString("cp"), rs.getInt("count(*)"));
      }
    } catch (Exception e) {
      System.err.println(e.getClass().getName() + ": " + e.getMessage());
      return gson.toJson(e.getMessage());
    } finally {

      if (rs != null) {
        try {
          rs.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

      if (stmt != null) {
        try {
          stmt.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

      if (c != null) {
        try {
          c.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

    }

    String json = gson.toJson(cp_count);

    return json;

  }


  @GetMapping("/stats")
  public String getStats() {

    Connection c = null;
    Statement stmt = null;
    ResultSet rs = null;
    Gson gson = new Gson();
    HashMap<String, Integer> maxCp = new HashMap<String, Integer>();
    HashMap<String, Integer> minCp = new HashMap<String, Integer>();
    Float avg = -1f;
    Double stdev = -1d;

    HashMap<String, Object> result = new HashMap<String, Object>();

    try {
      Class.forName("org.sqlite.JDBC");
      c = DriverManager.getConnection(dbpath);
      
      System.out.println("Opened database successfully");
      stmt = c.createStatement();

      System.out.println("accessing db");
      rs = stmt.executeQuery("SELECT cp, max(count) FROM (SELECT cp, count(*) as count FROM location_location GROUP BY(cp));");

      while (rs.next()) {
        maxCp.put(rs.getString("cp"), rs.getInt("max(count)"));
      }
      rs.close();

      rs = stmt.executeQuery("SELECT cp, min(count), avg(count) FROM (SELECT cp, count(*) as count FROM location_location GROUP BY(cp));");
      while (rs.next()) {
        minCp.put(rs.getString("cp"), rs.getInt("min(count)"));
        avg = rs.getFloat("avg(count)");

      }
      rs.close();

      rs = stmt.executeQuery("SELECT count(*) FROM location_location group by(cp);");

      int total = 0; //∑(xi-μ)^2
      int count = 0; //N
      while (rs.next()) {
        count += 1;
        total = total + (int)Math.pow(rs.getInt("count(*)")-avg, 2);
      }

      //sqrt(variance)
      stdev = Math.sqrt(total/count);

      result.put("max", maxCp);
      result.put("min", minCp);
      result.put("avg", avg);
      result.put("stdev", stdev);
      
    } catch (Exception e) {
      System.err.println(e.getClass().getName() + ": " + e.getMessage());
      return gson.toJson(e.getMessage());
    } finally {

      if (rs != null) {
        try {
          rs.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

      if (stmt != null) {
        try {
          stmt.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

      if (c != null) {
        try {
          c.close();
        } catch (Exception e) {
          e.printStackTrace();
        }
      }

    }

    
    String json = gson.toJson(result);

    return json;

  }


}