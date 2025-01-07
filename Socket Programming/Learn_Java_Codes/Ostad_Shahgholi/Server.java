/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javaapplication4;
import java.net.*;
import java.io.*;

/**
 *
 * @author Behrouz
 */


public class Server {
    public static void main(String[] args) {
       try{
          ServerSocket s=new ServerSocket(2000);
          int i=0;
          while (i<3){
              System.out.println("server wait");
              Socket client= s.accept();
              System.out.println(client.getLocalPort()+" "+ client.getPort());
              //client.close();
              Thread1 t=new Thread1(client);
              t.start();
              i++;
          }
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}

class Thread1 extends Thread {
    private Socket s;
    public Thread1(Socket s){
        this.s=s;
    }
    public void run(){
        try {
            InputStream i=s.getInputStream() ;
          
            DataOutputStream out=new DataOutputStream(s.getOutputStream());
            out.writeInt(70000);
            
            DataInputStream is=new DataInputStream(i);
            System.out.println(is.readLine());      
            
            ObjectInputStream  ois = new ObjectInputStream(i);
            Test t= (Test) ois.readObject();
            t.print();                     
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}