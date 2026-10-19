import java.nio.file.*;
import java.util.*;
import dev.ftb.mods.ftblibrary.snbt.SNBT;
import net.minecraft.nbt.*;

/** Compare a published quest to FTB's saved form without bootstrapping a game. */
public class QuestRewriteCheck {
    static Tag normalize(Tag input,String context) {
        if(input instanceof CompoundTag c) {
            CompoundTag out=new CompoundTag();
            for(String k:c.getAllKeys()) {
                Tag value=c.get(k);
                if(value instanceof ListTag l && l.isEmpty() && Set.of("images","quest_links","dependencies").contains(k))continue;
                if(k.equals("count") && value instanceof NumericTag n && n.getAsDouble()==1 && (context.equals("icon") || context.equals("tasks")))continue;
                out.put(k,normalize(value,k));
            }
            return out;
        }
        if(input instanceof ListTag l) {
            ListTag out=new ListTag();for(Tag t:l)out.add(normalize(t,context));return out;
        }
        return input.copy();
    }
    public static void main(String[] args)throws Exception {
        Path previous=Path.of(args[0]),live=Path.of(args[1]);int count=0;
        try(var files=Files.list(previous)) {
            for(Path p:files.filter(p->p.getFileName().toString().startsWith("local_guide_")).toList()) {
                var a=SNBT.tryRead(p);var b=SNBT.tryRead(live.resolve(p.getFileName()));
                if(a==null||b==null||!normalize(a,"root").equals(normalize(b,"root")))throw new AssertionError("Substantive change: "+p.getFileName());
                count++;
            }
        }
        if(count!=10)throw new AssertionError("Expected ten chapters");
        System.out.println("PASS: all ten saved chapters equal their published content after only empty-list and default-count normalization.");
    }
}
