/*s
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

public class UDPServer {
    public static void main(String[] args) {
       try{
          //DatagramSocket s=new DatagramSocket(2000);
          MulticastSocket s=new MulticastSocket(2000);
          s.joinGroup(InetAddress.getByName("225.1.1.1"));
          //first get its len
          while(true){
          byte data[]=new byte[4];
          DatagramPacket p=new DatagramPacket(data, 4);
          System.out.println("server wait1");
          s.receive(p);
          System.out.println(p.getPort());
          int len = 0;
          // byte[] -> int
          for (int i = 0; i < 4; ++i) {
              len |= (data[3-i] & 0xff) << (i << 3);
          }
          //NOW get the obj
          byte buf[]=new byte[len];
          DatagramPacket p2=new DatagramPacket(buf, len);
          System.out.println("server wait2 for "+len +"bytes");
          s.receive(p2);
          
          ByteArrayInputStream bis=new ByteArrayInputStream(buf);
          
          ObjectInputStream ois=new ObjectInputStream(bis);
          Test t= (Test) ois.readObject();
          t.print();
          //System.out.println(t);
          }       
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}
