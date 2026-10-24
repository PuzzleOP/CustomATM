import java.nio.file.*;
import net.minecraft.nbt.TagParser;
import dev.ftb.mods.ftblibrary.snbt.SNBT;

/** Parser-only validation; no game bootstrap, window, server or world. */
public class QuestSnbtCheck {
    public static void main(String[] args) throws Exception {
        int count=0;
        for(String dir:args) {
            try(var paths=Files.list(Path.of(dir))) {
                for(Path p:paths.filter(p->p.getFileName().toString().startsWith("local_guide_") && p.toString().endsWith(".snbt")).toList()) {
                    TagParser.parseTag(Files.readString(p));
                    if(SNBT.tryRead(p)==null)throw new AssertionError("FTB parser failed: "+p);
                    count++;
                }
            }
        }
        if(count!=22)throw new AssertionError("Expected 22 chapter/language files, got "+count);
        System.out.println("PASS: all 22 generated files parse with Minecraft and FTB SNBT parsers (no game started).");
    }
}
