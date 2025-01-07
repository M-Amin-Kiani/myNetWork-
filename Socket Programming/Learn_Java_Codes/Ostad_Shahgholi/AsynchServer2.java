/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication4;

import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
public class AsynchServer2 {   
    static AsynchronousServerSocketChannel serverChannel ;
    static AsynchronousSocketChannel clientChannel;
 public static void main(String [] s){
 try{
   serverChannel = AsynchronousServerSocketChannel.open();
   InetSocketAddress hostAddress = new InetSocketAddress("127.0.0.1", 2000);
   serverChannel.bind(hostAddress); 
  
    serverChannel.accept(
      null, new CompletionHandler<AsynchronousSocketChannel,Object>() {
 
        @Override
        public void completed(
          AsynchronousSocketChannel result, Object attachment) {
            if (serverChannel.isOpen()){              
                serverChannel.accept(null, this);
            }
            System.out.println("one connection accepted");
            clientChannel = result;
            if ((clientChannel != null) && (clientChannel.isOpen())) {
                ReadWriteHandler handler = new ReadWriteHandler();
                ByteBuffer buffer = ByteBuffer.allocate(32);
 
                HashMap <String , Object> readInfo = new HashMap();
                readInfo.put("action", "read");
                readInfo.put("buffer", buffer);

                clientChannel.read(buffer, readInfo, handler);
             }
         }
         @Override
         public void failed(Throwable exc, Object attachment) {
             // process error
         }
    });
     while (true) {
         Thread.sleep(1000);
        System.out.println("doing other work");
    }
 }catch (Exception e){
    
 }
}
 static class ReadWriteHandler implements
  CompletionHandler<Integer, Map<String, Object>> {
     
    @Override
    public void completed(
      Integer result, Map<String, Object> attachment) {
        Map<String, Object> actionInfo = attachment;
        String action = (String) actionInfo.get("action");
        if ("read".equals(action)) {
            ByteBuffer buffer = (ByteBuffer) actionInfo.get("buffer");
            System.out.println(new String(buffer.array()).trim());
            buffer.flip();
            actionInfo.put("action", "write");
            clientChannel.write(buffer, actionInfo, this);
            buffer.clear();
        } else if ("write".equals(action)) {
            ByteBuffer buffer = ByteBuffer.allocate(32);
            actionInfo.put("action", "read");
            actionInfo.put("buffer", buffer);
            clientChannel.read(buffer, actionInfo, this);
        }
    }     
    @Override
    public void failed(Throwable exc, Map<String, Object> attachment) {
        // 
    }
}
}

